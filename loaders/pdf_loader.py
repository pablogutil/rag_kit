from unstructured.partition.pdf import partition_pdf

def load_pdf(file_path: str) -> str:
    elements = partition_pdf(file_path)
    return "\n\n".join([str(element) for element in elements])