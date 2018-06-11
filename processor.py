import xml.etree.ElementTree as ET
import os

# TODO: Hacer expresión regular para quitar etiquetas html del texto de la clasificación CIP
# TODO: Adecuar para obtener archivos de carpetas por año


def get_xml_file(name, year):
    try:
        tree = ET.parse("patents_xml/" + year + "/" + name)
        root = tree.getroot()
    except FileNotFoundError:
        print("FILE", name, "NOT FOUND")
        root = False
    return root


def search_patents_in_tree(root):
    for child in root:
        t = child.attrib
        if t['nombre'] == "Patentes":
            patents = child
            return patents


def field_formatter(root):
    root_attr = root.attrib
    fields_l = ["Número de concesión", "Tipo de documento", "Número de solicitud", "Fecha de presentación", "Fecha de concesión",
                "Clasificación CIP", "Título", "Resumen", "Inventor(es)", "Titular"]
    fields_iter = iter(fields_l)
    patents = search_patents_in_tree(root)
    current_field = fields_iter.__next__()
    data = "Gaceta: " + root_attr['gaceta'] + " Volúmen: " + root_attr['volumen'] + "\n"  # Get type of document and
    #  month from root tag attrib
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
            if key in current_field:
                value = field.find("valor").text
                try:
                    data += value + '|'
                except TypeError:
                    data += " |"
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
    for year in range(2009, 2019):
        os.mkdir("output_files/" + str(year) + "/")
        for month in range(1, 13):
            if month > 9:
                base = "PA_RE_" + str(year) + '_' + str(month) + "_001.xml"
            else:
                base = "PA_RE_" + str(year) + '_0' + str(month) + "_001.xml"
            root = get_xml_file(base, str(year))
            if not root:
                continue
            data = field_formatter(root)
            out_name = base[:-4] + ".csv"
            f_out = open("output_files/" + str(year) + "/" + out_name, "w")
            f_out.write("Número de concesión|Tipo de documento|Número de solicitud|Fecha de presentación|"
                        "Fecha de concesión|Clasificación CIP|Título|Resumen|Inventor(es)|Titular\n")  # Header
            f_out.write(data)


if __name__ == '__main__':
    main()
