// docs/javascripts/mermaid-init.js
document.addEventListener("DOMContentLoaded", function() {
    mermaid.initialize({
        startOnLoad: true,
        theme: "default",
        securityLevel: "loose",
        flowchart: {
            useMaxWidth: false,
            htmlLabels: true,
            curve: 'basis'
        },
        sequence: {
            diagramMarginX: 50,
            diagramMarginY: 10,
            boxMargin: 10,
            showSequenceNumbers: false
        },
        gantt: {
            titleTopMargin: 25,
            barHeight: 20,
            barGap: 4,
            topPadding: 50,
            leftPadding: 75,
            gridLineStartPadding: 35,
            fontSize: 13,
            numberSectionStyles: 4,
            axisFormat: '%Y-%m-%d'
        }
    });
    
    // Re-render Mermaid diagrams when tabs are changed
    document.querySelectorAll('.md-tabs__link').forEach(tab => {
        tab.addEventListener('click', () => {
            setTimeout(() => {
                mermaid.init(undefined, '.mermaid');
            }, 300);
        });
    });
});
