import xml.etree.ElementTree as ET
import ast

def extract_node_properties_by_name(ows_path, target_name):
    """🔍 Extraction des propriétés pour un seul type de widget."""
    return extract_node_properties_by_names(ows_path, [target_name])


def extract_node_properties_by_names(ows_path, target_names):
    """🔍 Extraction des propriétés pour plusieurs types de widgets."""
    print(f"🔍 Lecture du fichier OWS : {ows_path}")
    tree = ET.parse(ows_path)
    root = tree.getroot()

    # Créer un mapping node_id -> name
    print("📦 Construction du mapping node_id -> node_name...")
    node_id_to_name = {
        node.attrib['id']: node.attrib.get('name', '')
        for node in root.find('nodes')
        if node.tag == 'node'
    }

    print(f"✅ {len(node_id_to_name)} nœuds détectés dans la section <nodes>.")

    results = []
    found = 0
    print(f"\n🔎 Recherche des propriétés pour les widgets : {target_names}")
    for prop in root.find('node_properties'):
        node_id = prop.attrib['node_id']
        node_name = node_id_to_name.get(node_id, '')
        if node_name in target_names:
            found += 1
            prop_text = prop.text.strip()
            print(f"\n📍 Propriétés trouvées pour node_id={node_id} ({node_name})")
            try:
                parsed_dict = ast.literal_eval(prop_text)
                results.append({
                    "node_id": node_id,
                    "node_name": node_name,
                    "properties": parsed_dict
                })
                print(f"✅ Contenu extrait (clé(s) : {list(parsed_dict.keys())}):\n{parsed_dict}")
            except Exception as e:
                print(f"❌ Erreur de parsing pour node_id={node_id}: {e}")
                print(f"Texte brut:\n{prop_text}")

    print(f"\n🎯 Total de nœuds correspondants : {found}")
    return results


# Exemple d'utilisation
if __name__ == "__main__":
    file = r"C:\Users\Admin\Downloads\toto_asssup.ows"

    # Pour un seul widget
    results_one = extract_node_properties_by_name(file, "S3 File Downloader")
    print(f"\n📋 Résultat [1 widget] : {len(results_one)} entrée(s) extraites.")

    # Pour plusieurs widgets
    widget_names = ["S3 File Downloader", "Directory Selector"]
    results_multi = extract_node_properties_by_names(file, widget_names)
    print(f"\n📋 Résultat [multi-widget] : {len(results_multi)} entrée(s) extraites.")
