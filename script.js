async function ingestData() {
    const urlsText = document.getElementById('urls').value;
    const urls = urlsText.split('\n').filter(url => url.trim());
    
    try {
        const response = await fetch('/ingest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ urls }),
        });
        
        const data = await response.json();
        alert(data.message);
    } catch (error) {
        alert('Error ingesting data: ' + error);
    }
}

async function searchQuery() {
    const query = document.getElementById('query').value;
    const responseDiv = document.getElementById('response');
    
    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            responseDiv.innerHTML = `<p>${data.response}</p>`;
        } else {
            responseDiv.innerHTML = `<p class="error">${data.message}</p>`;
        }
    } catch (error) {
        responseDiv.innerHTML = `<p class="error">Error: ${error}</p>`;
    }
}
