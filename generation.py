def parse_filename(filename):
    """
    Parse the filename to extract the title and abstract.
    
    Args:
        filename (str): The name of the file to parse.
    
    Returns:
        output (str): The filename with spaces replaced by underscores.
    """
    return filename.replace(' ', '_')

def create_txt(input_filename,title,abstract,output_filename):
    """
    Create a text file with the given filename, title, and abstract.
    
    Args:
        input_filename (str): The name of the input file.
        title (str): The title to include in the file.
        abstract (str): The abstract to include in the file.
    """
    with open(output_filename, 'w') as f:
        f.write(input_filename + '\n')
        if title != None : f.write(title + '\n')
        if abstract != None : f.write(abstract + '\n')


# Example usage:
#create_txt("example test file.pdf", "Example Title", "This is an example abstract.", parse_filename("example test file.pdf"))