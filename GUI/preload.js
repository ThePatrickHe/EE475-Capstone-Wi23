const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('main', {
  playback: (control) => ipcRenderer.invoke('playback', control),
  loadPage: (pagePath) => ipcRenderer.invoke('loadPage', pagePath),
  readFile: () => ipcRenderer.invoke('readFile'),
  spotifyRequest: (method, url, body) =>
    ipcRenderer.invoke('spotifyRequest', method, url, body),
});
