// Helper function to recursively extract visible text from DOM elements
// Handles text nodes, element nodes, and checks visibility
function getVisibleText(element) {
    // If it's a text node, return its trimmed content
    if (element.nodeType === Node.TEXT_NODE) {
        return element.textContent.trim();
    }
    // Skip non-element nodes
    if (element.nodeType !== Node.ELEMENT_NODE) {
        return '';
    }

    // Check if element is hidden via CSS
    const style = window.getComputedStyle(element);
    if (style.display === 'none' || style.visibility === 'hidden') {
        return '';
    }

    // Recursively process all child nodes
    let text = '';
    for (let child of element.childNodes) {
        text += getVisibleText(child);
    }
    return text;
}

// Helper function to convert relative URLs to absolute URLs
function getAbsoluteUrl(relativeUrl) {
    const a = document.createElement('a');
    a.href = relativeUrl;
    return a.href;
}

// Initialize result string
let result = '';

// Select all GitHub repository content containers
const containers = document.querySelectorAll('.Box-row');

// Process each container
containers.forEach(container => {
    // Extract and normalize visible text (remove extra whitespace)
    const visibleText = getVisibleText(container).replace(/\s+/g, ' ').trim();

    // Get all relevant links, excluding stargazers and forks
    const links = Array.from(container.querySelectorAll('a.Link'))
        .map(a => getAbsoluteUrl(a.getAttribute('href')))
        .filter(href => href && !href.endsWith('/stargazers') && !href.endsWith('/forks'));

    // Format the output with newlines
    result += visibleText + '\n';
    links.forEach(link => {
        result += link + '\n';
    });
    result += '\n';
});

// Return the final formatted string with any trailing whitespace removed
return result.trim();

