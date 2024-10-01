import lxml.etree as ET


def sum_synchronous_machine_ratedS(xml_file_path):
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

        # Define parent elements of interest
        parent_element = 'SynchronousMachine'

        # Find ratedS elements with specific parent
        rated_s_elements = root.xpath(f".//cim:{parent_element}/*[contains(local-name(), 'ratedS')]",
                                      namespaces=namespaces)

        total_capacity = 0

        if rated_s_elements:
            print(f"Found {len(rated_s_elements)} 'ratedS' element(s) under '{parent_element}'")
            for i, el in enumerate(rated_s_elements, 1):
                value = float(el.text)
                total_capacity += value

                parent_element_el = el.getparent()
                parent_name_el = parent_element_el.find('cim:IdentifiedObject.name', namespaces=namespaces)
                parent_name = parent_name_el.text if parent_name_el is not None else "Unknown"
                print(f"Element {i}: Parent({parent_element}), Name({parent_name}), Rated S: {value} MW")

            print(f"\nTotal production capacity of the generators in the model is: {total_capacity} MW")
        else:
            print(f"No 'ratedS' element found under '{parent_element}'")

    except ET.XMLSyntaxError as e:
        print(f"Error parsing XML: {e}")


# Example usage
xml_file_path = r'C:\Users\ungur\Desktop\Kool\Töö\Baltic RCC\Test 2\20210325T1530Z_1D_NL_EQ_001.xml'
sum_synchronous_machine_ratedS(xml_file_path)
