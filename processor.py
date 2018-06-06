import xml.etree.ElementTree as ET

# TODO: Hacer expresión regular para quitar etiquetas html del texto de la clasificación CIP
# TODO: Adecuar para obtener archivos de carpetas por año

def get_xml_file(name):
    tree = ET.parse("patents_xml/"+name)
    return tree.getroot()


def search_patents_in_tree(root):
    for child in root:
        t = child.attrib
        if t['nombre'] == "Patentes":
            patents = child
            return patents


def field_formatter(root):
    data = ""
    fields_l = ["Número de concesión", "Tipo de documento", "Número de solicitud", "Fecha de presentación", "Fecha de concesión",
                "Clasificación CIP", "Título", "Resumen", "Inventor(es)", "Titular"]
    fields_iter = iter(fields_l)
    patents = search_patents_in_tree(root)
    current_field = fields_iter.__next__()
    for patent in patents:
        fields_from_file = patent.findall("campo")
        fields_from_file_iter = iter(fields_from_file)
        while True:
            try:
                field = fields_from_file_iter.__next__()
            except StopIteration:
                print(current_field, "not found at this patent")
                data += "NF|"
                fields_from_file_iter = iter(fields_from_file)
            key = field.find("clave").text
            if key == current_field:
                value = field.find("valor").text
                data += value + '|'
                fields_from_file_iter = iter(fields_from_file)  # Rewind the fields where search
                try:
                    current_field = fields_iter.__next__()
                except StopIteration:
                    break
        fields_iter = iter(fields_l)
        current_field = fields_iter.__next__()
        data += '\n'
    return data


def main():
    year = "2017"
    for month in range(1, 13):
        if month > 9:
            base = "PA_RE_" + year + '_' + str(month) + "_001.xml"
        else:
            base = "PA_RE_" + year + '_0' + str(month) + "_001.xml"
        root = get_xml_file(base)
        data = field_formatter(root)
        out_name = base[:-4] + ".csv"
        f_out = open("output_files/" + out_name, "w")
        f_out.write("Número de concesión|Tipo de documento|Número de solicitud|Fecha de presentación|"
                    "Fecha de concesión|Clasificación CIP|Título|Resumen|Inventor(es)|Titular\n")  # Header
        f_out.write(data)


if __name__ == '__main__':
    main()
