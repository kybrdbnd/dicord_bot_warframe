def get_relics_drop_locations(components):
    dropLocations = []
    for component in components:
        if 'drops' in component:
            dropLocations.extend(list(map(lambda x: ' '.join(x['location'].split(' ')[:-1]), component['drops'])))
    return sorted(set(dropLocations))


def get_drop_locations(drops):
    dropValue = ''
    for drop in drops[:-5]:
        for key, values in drop.items():
            dropValue += f"**{key.title()}:** {values}\n"
        dropValue += '\n'
    return dropValue


def get_build_requirements(components):
    buildRequirementsValue = " "
    for component in components:
        buildRequirementsValue += f"**{component['name']}:** {component['itemCount']}\n"
    return buildRequirementsValue


def get_stats(levelStats):
    statsValues = " "
    i = 0
    for stat in levelStats:
        statsValues += f"**Level {i + 1}**: {', '.join(stat['stats'])}\n"
        i += 1
    return statsValues
