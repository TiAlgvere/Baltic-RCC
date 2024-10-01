import lxml.etree as ET

def find_nominal_voltages(xml_file_path, transformer_name):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Define namespaces for querying
        namespaces = {
            'cim': 'http://iec.ch/TC57/CIM100#',
            'md': 'http://iec.ch/TC57/61970-552/ModelDescription/1#',
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'eu': 'http://iec.ch/TC57/CIM100-European#'
        }

        # Find all PowerTransformerEnd elements associated with the given transformer
        nominal_voltages = []
        for end in root.xpath(".//cim:PowerTransformerEnd", namespaces=namespaces):
            name = end.find('cim:IdentifiedObject.name', namespaces)
            if name is not None and name.text == transformer_name:
                rated_u = end.find('cim:PowerTransformerEnd.ratedU', namespaces)
                if rated_u is not None:
                    nominal_voltages.append(float(rated_u.text))

        return nominal_voltages

    except ET.XMLSyntaxError as e:
        print(f"Error parsing XML: {e}")
        return []

# Example usage
xml_file_path = r'C:\Users\ungur\Desktop\Kool\Töö\Baltic RCC\Test 2\20210325T1530Z_1D_NL_EQ_001.xml'
transformer_name = 'NL_TR2_2'

# Find nominal voltages
nominal_voltages = find_nominal_voltages(xml_file_path, transformer_name)
print(f"Nominal Voltages of the windings of transformer {transformer_name}: {nominal_voltages} kV")
