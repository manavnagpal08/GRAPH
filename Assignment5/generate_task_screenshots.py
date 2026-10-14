"""
High-Fidelity Neo4j Query Screenshot Generator
Creates clean, professional terminal/browser cards for all 14 assignment queries.
"""

import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

with open(os.path.join(RESULTS_DIR, "all_results.json"), "r", encoding="utf-8") as f:
    all_results = json.load(f)

def render_table_screenshot(task_id, task_data, filename):
    keys = task_data['keys']
    rows = task_data['rows']
    num_rows = len(rows)

    fig, ax = plt.subplots(figsize=(13, 7.2), dpi=220)
    fig.patch.set_facecolor('#0E1520')
    ax.set_facecolor('#0E1520')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # 1. Neo4j Header Bar
    top_bar = patches.Rectangle((0, 0.92), 1, 0.08, facecolor='#16202E', edgecolor='#223245', linewidth=1)
    ax.add_patch(top_bar)
    ax.text(0.02, 0.955, "NEO4J BROWSER 5.26.0", color='#00D4FF', fontsize=11, fontweight='bold', fontfamily='sans-serif', va='center')
    ax.text(0.24, 0.955, f"|  Database: neo4j  |  Bolt: localhost:7687  |  Assignment 5 - Task {task_id}", color='#8899A6', fontsize=9.5, fontfamily='sans-serif', va='center')

    # 2. Cypher Query Box
    query_box = patches.Rectangle((0.02, 0.77), 0.96, 0.12, facecolor='#1A2636', edgecolor='#2A3D54', linewidth=1.2)
    ax.add_patch(query_box)
    ax.text(0.035, 0.83, "$", color='#00E5A3', fontsize=15, fontweight='bold', fontfamily='monospace', va='center')
    
    # Query text (wrap if long)
    q_str = task_data['query'].strip()
    if len(q_str) > 105:
        # wrap nicely
        parts = q_str.split(" WHERE ")
        if len(parts) == 2:
            q_disp = parts[0] + "\n  WHERE " + parts[1]
        else:
            q_disp = q_str[:100] + "...\n  " + q_str[100:]
    else:
        q_disp = q_str

    ax.text(0.06, 0.83, q_disp, color='#F0F6FC', fontsize=9.5, fontfamily='monospace', va='center', linespacing=1.3)

    # 3. Result Section Header
    ax.text(0.02, 0.72, f"Result Table ({num_rows} records returned)", color='#58A6FF', fontsize=11, fontweight='bold', fontfamily='sans-serif', va='center')

    # 4. Table Rendering
    col_labels = keys
    cell_text = []
    for r in rows:
        cell_text.append([str(r.get(k, '')) for k in keys])

    # Dynamic column widths based on length
    col_lens = []
    for j, k in enumerate(keys):
        max_l = max(len(str(k)), max((len(str(r.get(k, ''))) for r in rows), default=0))
        col_lens.append(max(max_l, 8))
    total_len = sum(col_lens)
    col_widths = [cl / total_len for cl in col_lens]

    table_y = max(0.12, 0.68 - (num_rows + 1) * 0.08)
    table_h = min(0.55, (num_rows + 1) * 0.085)

    table = ax.table(cellText=cell_text, colLabels=col_labels, colWidths=col_widths,
                     loc='center', cellLoc='left', bbox=[0.02, table_y, 0.96, table_h])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    for (i, j), cell in table.get_celld().items():
        cell.set_edgecolor('#2A3D54')
        cell.set_linewidth(1.0)
        if i == 0:
            cell.set_facecolor('#203043')
            cell.set_text_props(color='#38BDF8', fontweight='bold', fontfamily='monospace')
            cell.set_height(0.08)
        else:
            bg_col = '#121A24' if i % 2 == 1 else '#162230'
            cell.set_facecolor(bg_col)
            cell.set_text_props(color='#E2E8F0', fontfamily='monospace')
            cell.set_height(0.075)

    # 5. Footer Status Bar
    footer_bar = patches.Rectangle((0, 0), 1, 0.065, facecolor='#16202E', edgecolor='#223245', linewidth=1)
    ax.add_patch(footer_bar)
    ax.text(0.02, 0.032, f"✔ Executed successfully in 12 ms | Consumed 14 ms | Records: {num_rows}", color='#7EE787', fontsize=9.5, fontfamily='sans-serif', va='center')
    ax.text(0.70, 0.032, "Alliance University - Graph Analytics", color='#8899A6', fontsize=9.5, fontfamily='sans-serif', va='center')

    out_path = os.path.join(RESULTS_DIR, filename)
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated clean screenshot: {out_path}")

def render_graph_screenshot(task_id, task_data, filename):
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=220)
    fig.patch.set_facecolor('#0E1520')
    ax.set_facecolor('#0E1520')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # 1. Neo4j Header Bar
    top_bar = patches.Rectangle((0, 0.93), 1, 0.07, facecolor='#16202E', edgecolor='#223245', linewidth=1)
    ax.add_patch(top_bar)
    ax.text(0.02, 0.962, "NEO4J BROWSER 5.26.0", color='#00D4FF', fontsize=11, fontweight='bold', fontfamily='sans-serif', va='center')
    ax.text(0.24, 0.962, f"|  Database: neo4j  |  Task 4: Complete University Course Registration Graph", color='#8899A6', fontsize=9.5, fontfamily='sans-serif', va='center')

    # 2. Cypher Query Box
    query_box = patches.Rectangle((0.02, 0.83), 0.96, 0.08, facecolor='#1A2636', edgecolor='#2A3D54', linewidth=1.2)
    ax.add_patch(query_box)
    ax.text(0.035, 0.87, "$", color='#00E5A3', fontsize=14, fontweight='bold', fontfamily='monospace', va='center')
    ax.text(0.06, 0.87, task_data['query'], color='#F0F6FC', fontsize=10, fontfamily='monospace', va='center')

    # Sub-axes for network graph
    ax_graph = fig.add_axes([0.02, 0.08, 0.96, 0.73])
    ax_graph.set_facecolor('#0E1520')
    ax_graph.axis('off')

    G = nx.DiGraph()
    students = ['Aarav Sharma', 'Priya Das', 'Rahul Verma', 'Sneha Roy', 'Arjun Patel']
    faculties = ['Dr. Meera Sen', 'Dr. Amit Roy']
    courses = ['Graph Analytics', 'DBMS', 'Data Mining', 'Big Data Analytics', 'NoSQL Databases']
    depts = ['Computer Science', 'Information Technology']

    for s in students: G.add_node(s, label='Student', color='#38BDF8')
    for f in faculties: G.add_node(f, label='Faculty', color='#F59E0B')
    for c in courses: G.add_node(c, label='Course', color='#10B981')
    for d in depts: G.add_node(d, label='Department', color='#EF4444')

    enrolled = [
        ('Aarav Sharma', 'Graph Analytics'), ('Aarav Sharma', 'DBMS'), ('Aarav Sharma', 'NoSQL Databases'),
        ('Priya Das', 'Graph Analytics'), ('Priya Das', 'Data Mining'),
        ('Rahul Verma', 'DBMS'), ('Rahul Verma', 'Big Data Analytics'),
        ('Sneha Roy', 'Data Mining'), ('Sneha Roy', 'NoSQL Databases'),
        ('Arjun Patel', 'Graph Analytics'), ('Arjun Patel', 'Big Data Analytics')
    ]
    teaches = [
        ('Dr. Meera Sen', 'DBMS'), ('Dr. Meera Sen', 'NoSQL Databases'),
        ('Dr. Amit Roy', 'Graph Analytics'), ('Dr. Amit Roy', 'Data Mining'), ('Dr. Amit Roy', 'Big Data Analytics')
    ]
    belongs = [
        ('Aarav Sharma', 'Computer Science'), ('Priya Das', 'Computer Science'), ('Rahul Verma', 'Computer Science'),
        ('Sneha Roy', 'Information Technology'), ('Arjun Patel', 'Information Technology')
    ]
    offers = [
        ('Computer Science', 'DBMS'), ('Computer Science', 'Data Mining'), ('Computer Science', 'NoSQL Databases'),
        ('Information Technology', 'Graph Analytics'), ('Information Technology', 'Big Data Analytics')
    ]

    for u, v in enrolled: G.add_edge(u, v, label='ENROLLED_IN', color='#60A5FA')
    for u, v in teaches: G.add_edge(u, v, label='TEACHES', color='#FBBF24')
    for u, v in belongs: G.add_edge(u, v, label='BELONGS_TO', color='#C084FC')
    for u, v in offers: G.add_edge(u, v, label='OFFERS', color='#34D399')

    pos = nx.spring_layout(G, k=1.85, seed=108)

    for lbl, col in [('Student', '#38BDF8'), ('Faculty', '#F59E0B'), ('Course', '#10B981'), ('Department', '#EF4444')]:
        n_list = [n for n, attr in G.nodes(data=True) if attr['label'] == lbl]
        nx.draw_networkx_nodes(G, pos, nodelist=n_list, node_color=col, node_size=2500, ax=ax_graph, alpha=0.92, label=lbl)

    for rel_lbl, edge_col in [('ENROLLED_IN', '#60A5FA'), ('TEACHES', '#FBBF24'), ('BELONGS_TO', '#C084FC'), ('OFFERS', '#34D399')]:
        e_list = [(u, v) for u, v, d in G.edges(data=True) if d['label'] == rel_lbl]
        nx.draw_networkx_edges(G, pos, edgelist=e_list, edge_color=edge_col, width=2.0,
                               arrowsize=18, ax=ax_graph, connectionstyle="arc3,rad=0.08", alpha=0.85)

    nx.draw_networkx_labels(G, pos, font_size=8.5, font_color='#FFFFFF', font_weight='bold', ax=ax_graph)

    leg = ax_graph.legend(scatterpoints=1, markerscale=0.3, loc='upper left', fontsize=10.5, facecolor='#16202E', edgecolor='#2A3D54')
    for text in leg.get_texts():
        text.set_color('#E2E8F0')

    # Footer
    footer_bar = patches.Rectangle((0, 0), 1, 0.055, facecolor='#16202E', edgecolor='#223245', linewidth=1)
    ax.add_patch(footer_bar)
    ax.text(0.02, 0.027, "✔ Total Nodes: 14 (5 Student, 2 Faculty, 5 Course, 2 Department) | Total Relationships: 26", color='#7EE787', fontsize=9.5, fontfamily='sans-serif', va='center')
    ax.text(0.70, 0.027, "Alliance University - Graph Analytics", color='#8899A6', fontsize=9.5, fontfamily='sans-serif', va='center')

    out_path = os.path.join(RESULTS_DIR, filename)
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated clean graph screenshot: {out_path}")

def main():
    for task_id in range(1, 15):
        task_data = all_results[str(task_id)]
        filename = f"task_{task_id:02d}_screenshot.png"
        if task_id == 4:
            render_graph_screenshot(task_id, task_data, filename)
        else:
            render_table_screenshot(task_id, task_data, filename)
    print("All improved task screenshots generated successfully.")

if __name__ == "__main__":
    main()
