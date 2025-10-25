document.addEventListener('DOMContentLoaded', function() {
   
    const textInput = document.getElementById('textInput');
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const clearBtn = document.getElementById('clearBtn');
    const exportBtn = document.getElementById('exportBtn');
    const resultsSection = document.getElementById('resultsSection');
    const loading = document.getElementById('loading');
    
   
    analyzeBtn.addEventListener('click', analyzeText);
    clearBtn.addEventListener('click', clearText);
    exportBtn.addEventListener('click', exportResults);
    
    
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#4361ee';
        uploadArea.style.background = '#f0f4ff';
    });
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#e9ecef';
        uploadArea.style.background = '#f8f9fa';
    });
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#e9ecef';
        uploadArea.style.background = '#f8f9fa';
        
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileUpload(e.target.files[0]);
        }
    });
    
    
    function handleFileUpload(file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            textInput.value = e.target.result;
            uploadArea.querySelector('p').innerHTML = `<i class="fas fa-check-circle"></i> ${file.name} uploaded successfully`;
        };
        
        reader.onerror = function() {
            alert('Error reading file. Please try again.');
        };
        
        reader.readAsText(file);
    }
    
    function analyzeText() {
        const text = textInput.value.trim();
        
        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }
        
        
        loading.style.display = 'block';
        resultsSection.style.display = 'none';
        
        
        const formData = new FormData();
        formData.append('text', text);
        
        if (fileInput.files.length) {
            formData.append('file', fileInput.files[0]);
        }
        
        
        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            
            if (data.error) {
                alert(data.error);
                return;
            }
            
            displayResults(data);
            resultsSection.style.display = 'block';
            
            
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            loading.style.display = 'none';
            console.error('Error:', error);
            alert('An error occurred while analyzing the text. Please try again.');
        });
    }
    
    function displayResults(data) {
        
        document.getElementById('wordCount').textContent = data.word_count.toLocaleString();
        document.getElementById('charCountWithSpaces').textContent = data.char_count_with_spaces.toLocaleString();
        document.getElementById('charCountWithoutSpaces').textContent = data.char_count_without_spaces.toLocaleString();
        document.getElementById('lineCount').textContent = data.line_count.toLocaleString();
        document.getElementById('paragraphCount').textContent = data.paragraph_count.toLocaleString();
        document.getElementById('sentenceCount').textContent = data.sentence_count.toLocaleString();
        document.getElementById('avgWordLength').textContent = data.avg_word_length;
        document.getElementById('readingTime').textContent = data.reading_time;
        
       
        const frequencyChart = document.getElementById('wordFrequencyChart');
        frequencyChart.innerHTML = '';
        
        if (data.most_common_words && data.most_common_words.length > 0) {
            const maxFrequency = data.most_common_words[0][1];
            
            data.most_common_words.forEach(item => {
                const [word, frequency] = item;
                const percentage = (frequency / maxFrequency) * 100;
                
                const frequencyItem = document.createElement('div');
                frequencyItem.className = 'frequency-item';
                
                frequencyItem.innerHTML = `
                    <div class="word-label">${word}</div>
                    <div class="frequency-bar-container">
                        <div class="frequency-bar" style="width: ${percentage}%">
                            ${frequency}
                        </div>
                    </div>
                `;
                
                frequencyChart.appendChild(frequencyItem);
            });
        } else {
            frequencyChart.innerHTML = '<p>No word frequency data available.</p>';
        }
    }
    
    function clearText() {
        textInput.value = '';
        fileInput.value = '';
        resultsSection.style.display = 'none';
        uploadArea.querySelector('p').innerHTML = `<i class="fas fa-cloud-upload-alt"></i> Drag & drop a file here or <span>browse</span>`;
    }
    
    function exportResults() {
        // Get all the result data
        const results = {
            wordCount: document.getElementById('wordCount').textContent,
            charCountWithSpaces: document.getElementById('charCountWithSpaces').textContent,
            charCountWithoutSpaces: document.getElementById('charCountWithoutSpaces').textContent,
            lineCount: document.getElementById('lineCount').textContent,
            paragraphCount: document.getElementById('paragraphCount').textContent,
            sentenceCount: document.getElementById('sentenceCount').textContent,
            avgWordLength: document.getElementById('avgWordLength').textContent,
            readingTime: document.getElementById('readingTime').textContent
        };
        
        
        let exportText = `WORDCOUNT PRO - TEXT ANALYSIS RESULTS\n`;
        exportText += `========================================\n\n`;
        exportText += `Word Count: ${results.wordCount}\n`;
        exportText += `Characters (with spaces): ${results.charCountWithSpaces}\n`;
        exportText += `Characters (without spaces): ${results.charCountWithoutSpaces}\n`;
        exportText += `Lines: ${results.lineCount}\n`;
        exportText += `Paragraphs: ${results.paragraphCount}\n`;
        exportText += `Sentences: ${results.sentenceCount}\n`;
        exportText += `Average Word Length: ${results.avgWordLength}\n`;
        exportText += `Reading Time: ${results.readingTime} minutes\n\n`;
        exportText += `Analyzed on: ${new Date().toLocaleString()}\n`;
        
        
        const blob = new Blob([exportText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'wordcount_analysis.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
});
