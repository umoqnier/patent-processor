import xml.etree.ElementTree as ET


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
    patents = search_patents_in_tree(root)
    for patent in patents:
        fields = patent.findall("campo")
        for field in fields:
            key = field.find("clave").text
            if key in fields_l:
                value = field.find("valor").text
                data += value + '|'
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
        f_out.write("Número de concesión|Tipo de documento|Número de solicitud|Fecha de presentación|Fecha de concesión|"
                "Clasificación CIP|Título|Resumen|Inventor(es)|Titular\n")  # Header
        f_out.write(data)


if __name__ == '__main__':
    main()