import rdflib

# Define the XML file path
xml_file_path = r"C:\Users\ungur\Desktop\Kool\Töö\Baltic RCC\Test 2\20210325T1530Z_1D_NL_EQ_001.xml"

# Initialize a graph
graph = rdflib.Graph()

# Load the XML file into the graph
try:
    graph.parse(xml_file_path)
    print(f"Successfully loaded XML file: {xml_file_path}")
except Exception as e:
    print(f"Error loading XML file: {e}")
    exit()

# Print the root element
root_element = graph.identifier
print(f"Root element: {root_element}")

# List all ACLineSegment subjects
cim_namespace = rdflib.Namespace("http://iec.ch/TC57/CIM100#")

# Fetch all subjects of type ACLineSegment
print("\nAvailable ACLineSegment IDs:")
ac_line_segment_ids = []  # List to store ACLineSegment IDs
for subject in graph.subjects(predicate=rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), object=cim_namespace.ACLineSegment):
    # Print the subject URI and extract the local ID
    local_id = subject.split('#')[-1] if '#' in str(subject) else subject.split('/')[-1]
    ac_line_segment_ids.append(local_id)
    print(f"ACLineSegment ID: {local_id}")

# Define the target ACLineSegment ID you want to find
target_ac_line_segment_local_id = "_e8acf6b6-99cb-45ad-b8dc-16c7866a4ddc"  # Change this as needed

# Fetch details of ACLineSegment using the local ID directly
found_ac_line_segment = None
for subject in graph.subjects(predicate=rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), object=cim_namespace.ACLineSegment):
    local_id = subject.split('#')[-1] if '#' in str(subject) else subject.split('/')[-1]
    if local_id == target_ac_line_segment_local_id:
        found_ac_line_segment = subject
        break

if found_ac_line_segment:
    print(f"ACLineSegment with ID {target_ac_line_segment_local_id} found.")
    # Now let's fetch all the properties for the found ACLineSegment
    for predicate, obj in graph.predicate_objects(subject=found_ac_line_segment):
        print(f"Predicate: {predicate}, Object: {obj}")
else:
    print(f"ACLineSegment with ID {target_ac_line_segment_local_id} not found.")
