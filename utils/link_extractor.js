// Select all 'a' tags and convert NodeList to Array for easier manipulation
const links = Array.from(document.querySelectorAll('a'));

// Create CSV lines with format: index,text,url
// Index starts at 1 for human-readable counting
// Each field is properly quoted for CSV format
const csvLines = links.map((link, index) => 
    `${index + 1},"${link.textContent.trim()}","${link.href}"`
);

// Sort by total string length (descending order)
// Longer strings typically indicate content-rich links like article titles
// This helps filter out short utility links like "Sign Out", "Menu", etc.
const sortedLines = csvLines.sort((a, b) => b.length - a.length);

// Take only the top 50 longest links
// This focuses on the most content-rich links
const topLines = sortedLines.slice(0, 50);

// Resort by original document order using the preserved index
// This maintains the natural flow/hierarchy of content on the page
const reorderedLines = topLines.sort((a, b) => {
    const indexA = parseInt(a.split(',')[0]);
    const indexB = parseInt(b.split(',')[0]);
    return indexA - indexB;
});

// Join all lines with newline character for CSV format
// Using explicit \n for consistent line endings
return reorderedLines.join('\n');

