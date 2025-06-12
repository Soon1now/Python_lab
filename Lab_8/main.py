import xml.etree.ElementTree as ET
from collections import Counter

tree = ET.parse('14.osm')
root = tree.getroot()

non_supermarkets = []

for element in root.findall('.//*'):
    if element.tag in ['node', 'way', 'relation']:
        shop_type = None

        for tag in element.findall('tag'):
            if tag.get('k') == 'shop':
                shop_type = tag.get('v')
                break

        if shop_type and shop_type != 'supermarket':
            non_supermarkets.append(shop_type)

total_count = len(non_supermarkets)
print(f"Количество магазинов, не являющихся супермаркетами: {total_count}")

shop_type_counter = Counter(non_supermarkets)

print("Типы магазинов и их количество:")
for shop_type, count in sorted(shop_type_counter.items()):
    print(f"{shop_type}: {count}")