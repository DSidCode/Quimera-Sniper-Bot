for filename in ['quimera_terminal.html', 'radar.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where the tbody block is
    if "if (tbody) { tbody.innerHTML = '';" in content:
        # we need to close the `if (tbody)` block right after `});` before `// Actualizar Panel de Alertas`
        content = content.replace("});\n                \n                // Actualizar Panel de Alertas", 
                                  "});\n                }\n                \n                // Actualizar Panel de Alertas")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

print("JS fixed.")
