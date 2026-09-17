import re

for filename in ['quimera_terminal.html', 'radar.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for null before updating sniper-body
    content = content.replace("const tbody = document.getElementById('sniper-body');\n                tbody.innerHTML = '';", 
                              "const tbody = document.getElementById('sniper-body');\n                if (tbody) { tbody.innerHTML = '';")
    
    # Close the if block after the forEach loop
    content = content.replace("});\n                \n                const alertsList", "});\n                }\n                \n                const alertsList")

    # Check for null before updating alerts-list
    content = content.replace("const alertsList = document.getElementById('alerts-list');\n                if (data.alerts",
                              "const alertsList = document.getElementById('alerts-list');\n                if (alertsList && data.alerts")
    content = content.replace("} else {\n                    alertsList.innerHTML",
                              "} else if (alertsList) {\n                    alertsList.innerHTML")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("JS patched safely.")
