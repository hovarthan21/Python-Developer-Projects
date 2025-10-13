
async function api(path, method='GET', body=null) {
  const opts = { method, headers: {} };
  if (body) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  }
  const res = await fetch(path, opts);
  return res.json();
}

const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const chooseBtn = document.getElementById('chooseBtn');
const fileList = document.getElementById('fileList');
const fileSelect = document.getElementById('fileSelect');
const fileContent = document.getElementById('fileContent');
const binaryNotice = document.getElementById('binaryNotice');
const statusBox = document.getElementById('statusBox');

const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');

const downloadBtn = document.getElementById('downloadBtn');
const deleteBtn = document.getElementById('deleteBtn');

const findInput = document.getElementById('findInput');
const replaceInput = document.getElementById('replaceInput');
const replaceAllCheckbox = document.getElementById('replaceAll');
const replaceBtn = document.getElementById('replaceBtn');

chooseBtn.addEventListener('click', (e) => { e.preventDefault(); fileInput.click(); });
fileInput.addEventListener('change', handleFiles);

dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.style.transform='translateY(-6px)'; });
dropzone.addEventListener('dragleave', (e) => { dropzone.style.transform=''; });
dropzone.addEventListener('drop', (e) => {
  e.preventDefault(); dropzone.style.transform='';
  const files = e.dataTransfer.files;
  if (files && files.length) uploadFile(files[0]);
});


loadFileList();

function handleFiles(e) {
  const f = e.target.files[0];
  if (!f) return;
  uploadFile(f);
  fileInput.value = '';
}


function uploadFile(file) {
  progressContainer.style.display = 'block';
  progressBar.style.width = '0%';
  progressBar.textContent = '0%';
  status('Uploading...', 'info');

  const url = '/upload';
  const form = new FormData();
  form.append('file', file);

  const xhr = new XMLHttpRequest();
  xhr.open('POST', url, true);

  xhr.upload.onprogress = function (e) {
    if (e.lengthComputable) {
      const percent = Math.round((e.loaded / e.total) * 100);
      progressBar.style.width = percent + '%';
      progressBar.textContent = percent + '%';
    }
  };

  xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
      const res = JSON.parse(xhr.responseText);
      if (res.success) {
        progressBar.style.width = '100%';
        progressBar.textContent = 'Completed';
        status(`Uploaded: ${res.filename}`, 'success');
        loadFileList();
      } else {
        status(res.error || 'Upload failed', 'error');
      }
    } else {
      status('Upload failed: ' + xhr.statusText, 'error');
    }
   
    setTimeout(() => {
      progressContainer.style.display = 'none';
      progressBar.style.width = '0%';
      progressBar.textContent = '';
    }, 900);
  };

  xhr.onerror = function () {
    status('Upload error', 'error');
    progressContainer.style.display = 'none';
  };

  xhr.send(form);
}

async function loadFileList() {
  const data = await api('/files');
  if (!data.success) { status('Could not list files', 'error'); return; }
  fileList.innerHTML = '';
  fileSelect.innerHTML = `<option value="">— Select file to preview —</option>`;
  data.files.forEach(fn => {
    const li = document.createElement('li');
    li.className = 'file-item';
    li.innerHTML = `<span class="meta">${fn}</span>
      <div>
        <button class="btn-open" data-f="${fn}">Open</button>
        <a class="btn-download" href="/download/${encodeURIComponent(fn)}">Download</a>
      </div>`;
    fileList.appendChild(li);
  });


  data.files.forEach(fn => {
    const opt = document.createElement('option');
    opt.value = fn; opt.textContent = fn;
    fileSelect.appendChild(opt);
  });


  document.querySelectorAll('.btn-open').forEach(b => b.addEventListener('click', () => {
    const f = b.dataset.f; loadFile(f);
  }));
}

async function loadFile(filename) {
  if (!filename) return;
  const res = await api('/read', 'POST', { filename });
  if (!res.success) { status(res.error || 'Read failed', 'error'); return; }

  if (res.content === null) {
    fileContent.value = '';
    binaryNotice.style.display = 'block';
  } else {
    fileContent.value = res.content;
    binaryNotice.style.display = 'none';
  }
  fileSelect.value = filename;
  status(`Loaded ${filename}`, 'success');
}

fileSelect.addEventListener('change', (e) => {
  const f = e.target.value;
  if (f) loadFile(f);
});

downloadBtn.addEventListener('click', () => {
  const f = fileSelect.value;
  if (!f) return status('Choose a file first', 'error');
  window.location = `/download/${encodeURIComponent(f)}`;
});

deleteBtn.addEventListener('click', async () => {
  const f = fileSelect.value;
  if (!f) return status('Choose a file first', 'error');
  if (!confirm(`Delete ${f}? This cannot be undone.`)) return;
  const res = await api('/delete', 'POST', { filename: f });
  if (res.success) {
    status('Deleted ' + f, 'success');
    fileContent.value = '';
    binaryNotice.style.display = 'none';
    loadFileList();
  } else {
    status(res.error || 'Delete failed', 'error');
  }
});

replaceBtn.addEventListener('click', async () => {
  const filename = fileSelect.value;
  const find = findInput.value;
  const replace = replaceInput.value;
  const replaceAll = replaceAllCheckbox.checked;

  if (!filename) return status('Select a file first', 'error');
  if (!find) return status('Enter text to find', 'error');

  status('Processing...', 'info');
  const res = await api('/find_replace', 'POST', { filename, find, replace, replace_all: replaceAll });
  if (res.success) {
    if (res.content !== undefined) fileContent.value = res.content;
    status(`Replaced ${res.replaced} occurrence(s)`, 'success');
  } else {
    status(res.error || 'Replace failed', 'error');
  }
});


function status(text, type='info') {
  const c = statusBox;
  c.textContent = text;
  c.style.color = type === 'error' ? '#ff3b5c' : type === 'success' ? '#0a8a4f' : '#333';
  c.style.background = type === 'info' ? 'rgba(0,0,0,0.03)' : 'transparent';
  if (type === 'success') {
    c.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.02)' }, { transform: 'scale(1)' }], { duration: 400 });
  }
}
