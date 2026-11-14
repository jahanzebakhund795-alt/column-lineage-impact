"""Column Lineage Impact Analyzer. Synthetic portfolio demonstration."""
def run(data):
    graph = {}
    for source,target in data['edges']:
        graph.setdefault(source,set()).add(target)
    visiting,done = set(),set()
    def visit(node):
        if node in visiting:
            raise ValueError('Lineage cycle detected')
        if node in done:
            return
        visiting.add(node)
        for target in graph.get(node,()):
            visit(target)
        visiting.remove(node)
        done.add(node)
    for node in graph:
        visit(node)
    impacted,queue = set(),[data['changed']]
    while queue:
        for target in graph.get(queue.pop(),()):
            if target not in impacted:
                impacted.add(target)
                queue.append(target)
    return {'changed':data['changed'],'impacted':sorted(impacted)}



if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('sample.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.input.read_text()))
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.write_text(serialized + '\n')
    else:
        print(serialized)
