// docs/javascripts/mermaid-init.js
document.addEventListener('DOMContentLoaded', function() {
    mermaid.initialize({
        startOnLoad: true,
        theme: 'dark',
        securityLevel: 'loose',
        flowchart: {
            useMaxWidth: false,
            htmlLabels: true
        },
        themeVariables: {
            primaryColor: '#5e35b1',
            primaryBorderColor: '#4527a0',
            primaryTextColor: '#ffffff'
        }
    });
    
    // Re-render les diagrammes quand on change d'onglet
    document.querySelectorAll('.md-tabs__link').forEach(tab => {
        tab.addEventListener('click', () => {
            setTimeout(mermaid.init, 300);
        });
    });
});