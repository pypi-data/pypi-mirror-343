import argparse
import gzip
import logging
import os
import re
import sys

logging.basicConfig(format="%(message)s", level=logging.INFO)
log = lambda message: logging.info(message)


VERSION = "2025-03-24"
HELP = f"""
Reformat RSEM output files.

Arguments:
  $1            Base path of RSEM output files.
  $2            Path to annotation file (gtf or gff3).
  -h --help     Print help message and exit.
  -v --version  Print version and exit (v. {VERSION}).
"""

GTF_GFF3_ATTRIBUTES = {
    "gtf": {
        "attributes_regex": re.compile(r"(\w+)\s+(?:\"([^\"]*)\"|([^;]+))"),
        "gene_id_field": "gene_id",
        "gene_name_field": "gene_name",
        "gene_type_field": "gene_type",
        "transcript_id_field": "transcript_id",
        "transcript_parent_field": "gene_id",
        "support_level_field": "transcript_support_level",
        "exon_id_field": "exon_number",
        "exon_parent_field": "transcript_id"},
    "gff3": {
        "attributes_regex": re.compile(r"(\w+)=([^;]*)"),
        "gene_id_field": "gene_id",
        "gene_name_field": "Name",
        "gene_type_field": "gene_type",
        "transcript_id_field": "transcript_id",
        "transcript_parent_field": "Parent",
        "support_level_field": "transcript_support_level",
        "exon_id_field": "exon_number",
        "exon_parent_field": "Parent"}}


def read_tsv(file_path, require_header=None):
    lines = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.rstrip()
            if not line:
                continue
            lines.append(line.split("\t"))
    data = {}
    for index, name in enumerate(lines[0]):
        data[name.lower()] = [line[index] for line in lines[1:]]
    if require_header:
        header = tuple(sorted(data.keys()))
        required = tuple(sorted(set(require_header)))
        if header != required:
            raise ValueError(f"header mismatch: {header} != {required}")
    return data


def open_compressed(path, mode="r", compression="auto", level=6, **open_kargs):
    modes = dict(
        ((first + second + third), (first + second + (third or "t")))
        for first in ("r", "w", "x", "a")
        for second in ("", "+")
        for third in ("", "t", "b"))
    mode = modes[mode]
    if not isinstance(compression, bool):
        if compression == "auto" and mode[0] in ("w", "x"):
            compression = "extension"
        compression = infer_compression(path, compression)
    if compression:
        return gzip.open(path, mode, level, **open_kargs)
    return open(path, mode, **open_kargs)


def infer_compression(path, mode="auto"):
    if mode == "extension":
        return path.lower().endswith(".gz")
    if mode == "magic":
        with open(path, "rb") as file:
            return file.read(2) == b"\x1f\x8b"
    if mode == "auto":
        try:
            return infer_compression(path, "magic")
        except Exception:
            return infer_compression(path, "extension")
    raise ValueError(f"infer mode {mode} invalid (auto, magic or extension)")


def iter_gtf_rows(path):
    with open_compressed(path, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            yield line


def parse_gtf_attributes(raw, regex, fix_fields=[]):
    attributes = dict(
        [value for value in match.groups() if value is not None]
        for match in regex.finditer(raw))
    for field in fix_fields:
        if field == "gene_type":
            if "gene_biotype" in attributes and "gene_type" not in attributes:
                attributes["gene_type"] = attributes["gene_biotype"]
                del attributes["gene_biotype"]
        else:
            value = attributes[field]
            if value[:11] == "transcript:":
                attributes[field] = value[11:]
            elif value[:5] == "gene:":
                attributes[field] = value[5:]
    return attributes


def read_gtf(path, format="infer"):
    """
    data = {chr_id, start, end, strand, gene_id, gene_name, gene_type, transcripts}
    with transcript as [start, end, transcript_id, support_level, exons]
    with exon as [start, end]
    """
    if format == "infer": format = \
        "gtf" if ".gtf" in path[-8:].lower() else \
        "gff3" if ".gff3" in path[-8:].lower() else \
        "unable_to_infer_format"
    format_attributes = GTF_GFF3_ATTRIBUTES[format]
    attributes_regex, gene_id_field, gene_name_field, gene_type_field, \
    transcript_id_field, transcript_parent_field, support_level_field, \
    exon_id_field, exon_parent_field = format_attributes.values()
    genes = {}
    transcripts = {}
    exons = {}
    annotations_types = set()
    genes_types = set()
    support_levels = set()
    for line in iter_gtf_rows(path):
        try:
            chr_id, _, annotation_type, rest = line.split("\t", 3)
            annotations_types.add(annotation_type)
            if annotation_type == "gene":
                start, end, _, strand, _, attributes = rest.split("\t", 5)
                start = int(start) - 1
                end = int(end)
                attributes = parse_gtf_attributes(attributes, attributes_regex, ["gene_type"])
                gene_id = attributes[gene_id_field]
                gene_name = attributes[gene_name_field] \
                    if gene_name_field in attributes \
                    else gene_id
                gene_type = attributes[gene_type_field]
                genes_types.add(gene_type)
                gene = [chr_id, start, end, strand, gene_id, gene_name, gene_type, []]
                genes[gene_id] = gene
                continue
            if annotation_type == "transcript":
                start, end, _, _, _, attributes = rest.split("\t", 5)
                start = int(start) - 1
                end = int(end)
                attributes = parse_gtf_attributes(attributes, attributes_regex, [transcript_parent_field])
                transcript_id = attributes[transcript_id_field]
                support_level = \
                    attributes[support_level_field] \
                    if support_level_field in attributes \
                    else "NA"
                support_levels.add(support_level)
                gene_id = attributes[transcript_parent_field]
                transcript = [start, end, transcript_id, support_level, []]
                transcripts[transcript_id] = [gene_id, transcript]
                continue
            if annotation_type == "exon":
                start, end, _, _, _, attributes = rest.split("\t", 5)
                start = int(start) - 1
                end = int(end)
                attributes = parse_gtf_attributes(attributes, attributes_regex, [exon_parent_field])
                transcript_id = attributes[exon_parent_field]
                exon_id = attributes[exon_id_field]
                exon = [start, end]
                exons[(transcript_id, exon_id)] = exon
                continue
        except Exception as error:
            line = line.strip().split("\t")
            raise RuntimeError(f"error on line {line}") from error
    for (transcript_id, exon_id), exon in exons.items():
        try:
            transcripts[transcript_id][1][4].append(exon)
        except KeyError as error:
            raise RuntimeError(f"no transcript for exon {transcript_id} {exon_id} {exon}") from error
    for gene_id, transcript in transcripts.values():
        transcript[4].sort(key=lambda exon: exon[1])
        transcript[4].sort(key=lambda exon: exon[0])
        try:
            genes[gene_id][7].append(transcript)
        except KeyError as error:
            line = line.strip().split("\t")
            raise RuntimeError(f"no gene for transcript {gene_id} {transcript}") from error
    for gene in genes.values():
        gene[7].sort(key=lambda transcript: transcript[1])
        gene[7].sort(key=lambda transcript: transcript[0])
    genes = sorted(genes.values(), key=lambda gene: gene[2])
    genes.sort(key=lambda gene: gene[1])
    genes.sort(key=lambda gene: gene[0])
    keys = "chr_id start end strand gene_id gene_name gene_type transcripts".split(" ")
    data = dict(zip(keys, zip(*genes)))
    info = \
        f"{len(genes):,} genes, " + \
        f"{len(transcripts):,} transcripts, " + \
        f"{len(exons):,} exons " + \
        f"(annotations: {' '.join(sorted(annotations_types))}, " \
        f"genes types: {' '.join(sorted(genes_types))}, " \
        f"support levels: {' '.join(sorted(support_levels))})"
    return data, info


def reformat_rsem(base_path, gtf_path):

    log(f"--- Reformat RSEM (v: {VERSION}) ---")
    log(f"Base path: {base_path}")
    log(f"Annotations: {gtf_path}")

    input_genes_header = "gene_id transcript_id(s) length effective_length expected_count tpm fpkm".split(" ")
    input_transcripts_header = "transcript_id gene_id length effective_length expected_count tpm fpkm isopct".split(" ")
    input_genes = read_tsv(f"{base_path}.genes.results", input_genes_header)
    input_transcripts = read_tsv(f"{base_path}.isoforms.results", input_transcripts_header)
    
    annotations, _ = read_gtf(gtf_path)
    genes_annotations = {
        gene_id: {key: annotations[key][gene_index] for key in annotations}
        for gene_index, gene_id in enumerate(annotations["gene_id"])}
    transcript_annotations = {
        transcript[2]: (gene_id, transcript)
        for gene_index, gene_id in enumerate(annotations["gene_id"])
        for transcript in annotations["transcripts"][gene_index]}

    output_genes_header = [
        "chr_id", "start", "end", "strand", "gene_id", "gene_name", "gene_type",
        "transcript_ids", "length", "effective_length", "expected_count", "fkpm", "tpm"]
    default_gene = dict((key, "#N/A") for key in output_genes_header)
    output_genes = []
    for gene_index, gene_id in enumerate(input_genes["gene_id"]):
        gene = genes_annotations.get(gene_id, default_gene)
        output_gene = [
            gene["chr_id"],
            gene["start"],
            gene["end"],
            gene["strand"],
            gene["gene_id"],
            gene["gene_name"],
            gene["gene_type"],
            input_genes["transcript_id(s)"][gene_index],
            input_genes["length"][gene_index],
            input_genes["effective_length"][gene_index],
            input_genes["expected_count"][gene_index],
            input_genes["fpkm"][gene_index],
            input_genes["tpm"][gene_index]]
        output_genes.append(output_gene)
    
    output_transcripts_header = [
        "chr_id", "start", "end", "strand", "gene_id", "gene_name", "gene_type",
        "transcript_id", "transcript_start", "transcript_end",
        "length", "effective_length", "expected_count", "fkpm", "tpm", "fraction"]
    output_transcripts = []
    for transcript_index, transcript_id in enumerate(input_transcripts["transcript_id"]):
        default_transcript = ("#N/A", ("#N/A", "#N/A", "#N/A", "#N/A", []))
        gene_id, transcript = transcript_annotations.get(transcript_id, default_transcript)
        gene = genes_annotations.get(gene_id, default_gene)
        output_transcript = [
            gene["chr_id"],
            gene["start"],
            gene["end"],
            gene["strand"],
            gene["gene_id"],
            gene["gene_name"],
            gene["gene_type"],
            transcript_id,
            transcript[0],
            transcript[1],
            input_transcripts["length"][transcript_index],
            input_transcripts["effective_length"][transcript_index],
            input_transcripts["expected_count"][transcript_index],
            input_transcripts["fpkm"][transcript_index],
            input_transcripts["tpm"][transcript_index],
            input_transcripts["isopct"][transcript_index]]
        output_transcripts.append(output_transcript)
    
    output_genes_path = f"{base_path}.genes.tsv"
    output_transcripts_path = f"{base_path}.transcripts.tsv"
    with open(output_genes_path, "w") as file:
        file.write("\t".join(output_genes_header) + "\n")
        for gene in output_genes:
            file.write("\t".join(map(str, gene)) + "\n")
    
    output_transcripts_path = f"{base_path}.transcripts.tsv"
    with open(output_transcripts_path, "w") as file:
        file.write("\t".join(output_transcripts_header) + "\n")
        for transcript in output_transcripts:
            file.write("\t".join(map(str, transcript)) + "\n")
    
    os.remove(f"{base_path}.genes.results")
    os.remove(f"{base_path}.isoforms.results")

    log("--- Reformat RSEM done ---")


def main(raw_args):
    if "-h" in raw_args or "--help" in raw_args:
        sys.stderr.write("{}\n".format(HELP.strip()))
        return
    if "-v" in raw_args or "--version" in raw_args:
        sys.stderr.write("{}\n".format(VERSION))
        return
    parser = argparse.ArgumentParser()
    parser.add_argument("base_path")
    parser.add_argument("gtf_path")
    args = vars(parser.parse_args(raw_args)).values()
    reformat_rsem(*args)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        log(f"Error: {e}")
