const DATA_DIR = '../scraped_data';

document.addEventListener('DOMContentLoaded', function () {
    const anchor = window.location.hash.substring(1);

    // Load CSV files
    loadCSV(DATA_DIR + '/scraped_companies.csv', 'companies');
    loadCSV(DATA_DIR + '/scraped_sites.csv', 'sites');
    loadCSV(DATA_DIR + '/scraped_contacts.csv', 'contacts');

    // Function to load CSV and render the table
    function loadCSV(file, type) {
        Papa.parse(file, {
            download: true,
            header: true,
            complete: function (results) {
                console.log(results)
                renderTable(results.data, type);
            },
            error: function(err) {
                console.error("Error loading CSV:", err);
            }
        });
    }

    // Function to render the table based on CSV data
    function renderTable(data, type) {
        let tableBody = document.querySelector(`#${type}-table tbody`);
        if (!tableBody) return;

        data.forEach((row) => {
            let tr = document.createElement('tr');
            tr.setAttribute('id', `row-${row['ID']}`)
            Object.keys(row).forEach((key) => {
                if (!key.startsWith('ID')) {
                    let td = document.createElement('td');
                    td.textContent = row[key];

                    // Link the site to its company based on 'Société'
                    if (key === 'Société' && type === 'sites') {
                        td.innerHTML = `<a href="companies.html#row-${row["ID Société"]}" target="_blank">${row[key]}</a>`;
                    }

                    // Link the contact to its site
                    if (key === 'Site' && type === 'contacts') {
                        td.innerHTML = `<a href="sites.html#row-${row["ID Site"]}" target="_blank"">${row[key]}</a>`;
                    }

                    tr.appendChild(td);
                }
            });
            tableBody.appendChild(tr);
        });

        // Scroll to the anchor (if exists) after rendering
        if (anchor) {
            scrollToAnchor(anchor);
        }
    }

    document.querySelectorAll('.search-fields input[type="text"]').forEach(input => {
        input.addEventListener('input', function () {
            const columnIndex = parseInt(this.getAttribute('data-search-index'));
            filterTable(columnIndex, this.value);
        });
    });

    // Filter function
    function filterTable(colIndex, query) {
        let tableBody = document.querySelector(`#table-container table tbody`);
        const rows = tableBody.querySelectorAll('tr');
        rows.forEach(row => {
            const cell = row.querySelectorAll('td')[colIndex];
            if (cell) {
                row.style.display = cell.textContent.toLowerCase().includes(query.toLowerCase()) ? '' : 'none';
            }
        });
    }

   // Scroll to the row that matches the anchor and apply the special style
   function scrollToAnchor(anchor) {
    const targetRow = document.getElementById(anchor);

    if (targetRow) {
        // Remove the 'selected-row' class from any previously selected row
        const previouslySelected = document.querySelector('.selected-row');
        if (previouslySelected) {
            previouslySelected.classList.remove('selected-row');
        }

        // Scroll to the target row and apply the special class
        const targetY = targetRow.getBoundingClientRect().top + window.scrollY;
        window.scrollTo({top: targetY-100, behavior: 'smooth'})
        targetRow.classList.add('selected-row'); // Add the special class to highlight the row
    }
}
});
