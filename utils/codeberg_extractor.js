// Helper function to convert relative URLs to absolute using current page origin
function getAbsoluteUrl(relativeUrl) {
    return new URL(relativeUrl, window.location.origin).href;
}

// Helper function to safely extract text content from elements
// Returns empty string if element not found
function extractText(element, selector) {
    const el = element.querySelector(selector);
    return el ? el.textContent.trim() : '';
}

// Select all repository containers and process each one
return Array.from(document.querySelectorAll('.flex-item')).map(container => {
    // Extract repository name elements and combine them into full path
    const nameElements = container.querySelectorAll('.flex-item-title .text.primary.name');
    const fullName = Array.from(nameElements)
        .map(el => el.textContent.trim())
        .join('/');

    // Get repository URL from the last name element
    const link = nameElements.length ? 
        getAbsoluteUrl(nameElements[nameElements.length - 1].getAttribute('href')) : '';

    // Extract additional metadata
    const description = extractText(container, '.flex-item-body');
    const language = extractText(container, '.flex-item-trailing .flex-text-inline');
    const updateTime = container.querySelector('.flex-item-body relative-time')
        ?.getAttribute('datetime') || '';

    // Combine all information into formatted string
    // Filter out empty strings and join with newlines
    return [
        fullName,
        link,
        description,
        language ? 'Language: ' + language : '',
        updateTime ? 'Updated: ' + updateTime : ''
    ].filter(Boolean).join('\n');
}).join('\n\n');

