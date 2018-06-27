import xml.etree.ElementTree as ET
import os

# TODO: Hacer expresión regular para quitar etiquetas html del texto de la clasificación CIP
# TODO: Adecuar para obtener archivos de carpetas por año


def get_fields(file_name):
    with open(file_name, "r") as f:
        data = f.readline()
        return data.split(',')


def get_xml_file(patent_type, name, year):
    try:
        tree = ET.parse("patents_xml/" + patent_type + '/' + year + '/' + name)
        root = tree.getroot()
    except FileNotFoundError:
        print("FILE", name, "NOT FOUND")
        root = False
    return root


def search_patents_in_tree(root):
    for child in root:
        t = child.attrib
        if t['nombre'] == "Patentes" or t['nombre'] == "Solicitudes normales":
            patents = child
            return patents


def field_formatter(root):
    root_attr = root.attrib
    fields_l = get_fields("campos_solicitadas.txt")
    fields_iter = iter(fields_l)
    patents = search_patents_in_tree(root)
    current_field = fields_iter.__next__()
    data = "Gaceta: " + root_attr['gaceta'] + " Volúmen: " + root_attr['volumen'] + "\n"  # Get type of document and
    #  month from root tag attrib
    for patent in patents:
        fields_from_xml = patent.findall("campo")
        fields_from_xml_iter = iter(fields_from_xml)
        while True:
            try:
                field = fields_from_xml_iter.__next__()
            except StopIteration:
                print(current_field, "not found at this patent")
                data += "NF|"
                fields_from_xml_iter = iter(fields_from_xml)
                try:
                    current_field = fields_iter.__next__()
                except StopIteration:
                    break
            key = field.find("clave").text
            if key == current_field:  # TODO: Solucion de conflictos con patentes que tienen nombres diferentes en campo
                value = field.find("valor").text
                try:
                    data += value + '|'
                except TypeError:
                    data += " |"
                fields_from_xml_iter = iter(fields_from_xml)  # Rewind the fields where search
                try:
                    current_field = fields_iter.__next__()
                except StopIteration:
                    break
        fields_iter = iter(fields_l)
        current_field = fields_iter.__next__()
        data += '\n'
    return data


def list_all_fields(root):
    patents = search_patents_in_tree(root)
    for patent in patents:
        fields = patent.findall("campo")
        for i, field in enumerate(fields):
            print(field.find("clave").text)
        break  # Just one patent


def main():
    print("¿Qué patentes deben ser procesadas?")
    mode = input("Solicitadas: (s) Otorgadas: (o) -->")
    for year in range(2009, 2019):
        if mode == 'o' or mode == 'O':
            os.mkdir("output_files/otorgadas/" + str(year) + "/")
            for month in range(1, 13):
                if month > 9:
                    base = "PA_RE_" + str(year) + '_' + str(month) + "_001.xml"
                else:
                    base = "PA_RE_" + str(year) + '_0' + str(month) + "_001.xml"
                root = get_xml_file("otorgadas", base, str(year))
                if not root:
                    continue
                data = field_formatter(root)
                out_name = base[:-4] + ".csv"
                f_out = open("output_files/otorgadas/" + str(year) + "/" + out_name, "w")
                f_out.write("Numero de concesion|Tipo de documento|Numero de solicitud|Fecha de presentacion|"
                            "Fecha de concesion|Clasificacion CIP|Título|Resumen|Inventor(es)|Titular\n")  # Header
                f_out.write(data)
                f_out.close()
        elif mode == 's' or mode == 'S':
            os.mkdir("output_files/solicitadas/" + str(year) + "/")
            for month in range(1, 13):
                if month > 9:
                    base = "PA_SO_" + str(year) + '_' + str(month) + "_001.xml"
                else:
                    base = "PA_SO_" + str(year) + '_0' + str(month) + "_001.xml"
                root = get_xml_file("solicitadas", base, str(year))
                if not root:
                    continue
                print(str(year))
                data = field_formatter(root)
                out_name = base[:-4] + ".csv"
                f_out = open("output_files/solicitadas/" + str(year) + "/" + out_name, "w")
                f_out.write("Número de solicitud|Fecha de presentación|Solicitante(s)|Inventor(es)|Agente|"
                            "Prioridad (es)|Clasificación|Título|Resumen|Número de solicitud internacional|"
                            "Fecha de presentación internacional|Número de publicación internacional|"
                            "Fecha de publicación internacional\n")  # Header
                f_out.write(data)
                f_out.close()
        else:
            print("ERROR: Elige una opción correcta --> (s) - (o)")
            print("Saliendo del programa...")


if __name__ == '__main__':
    main()
