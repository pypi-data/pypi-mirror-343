"use strict";
(self["webpackChunkquapp_jupyterlab_s3_bridge"] = self["webpackChunkquapp_jupyterlab_s3_bridge"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _versions_dropdown__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./versions_dropdown */ "./lib/versions_dropdown.js");
/* harmony import */ var _save_button__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./save_button */ "./lib/save_button.js");
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./toolbar */ "./lib/toolbar.js");





const plugin = {
    id: 'quapp_jupyterlab_s3_bridge:plugin',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__.IFileBrowserFactory],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    activate: (app, factory, settingRegistry) => {
        console.log('JupyterLab S3 extension activated.');
        if (settingRegistry) {
            void settingRegistry.load(plugin.id).then((settings) => {
                console.log('Settings:', settings.composite);
            });
        }
        function enhanceBrowser(browserId) {
            const browser = factory.tracker.find((b) => b.id === browserId);
            if (!browser)
                return;
            const dropdown = new _versions_dropdown__WEBPACK_IMPORTED_MODULE_2__.VersionsDropdownWidget();
            const saveBtn = (0,_save_button__WEBPACK_IMPORTED_MODULE_3__.createSaveToS3Button)(() => dropdown.refresh());
            const toolbar = (0,_toolbar__WEBPACK_IMPORTED_MODULE_4__.createVersionToolbar)(dropdown);
            setTimeout(() => {
                if (!browser.toolbar.node.querySelector('#saveS3Button')) {
                    browser.toolbar.insertItem(1, 'saveS3', saveBtn);
                    browser.layout.insertWidget(1, toolbar);
                }
            }, 100);
        }
        factory.tracker.forEach((browser) => enhanceBrowser(browser.id));
        factory.tracker.widgetAdded.connect((_, browser) => enhanceBrowser(browser.id));
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/save_button.js":
/*!****************************!*\
  !*** ./lib/save_button.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createSaveToS3Button: () => (/* binding */ createSaveToS3Button)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);
// File: save_button.ts



// function getXsrfToken(): string {
//   const matches = document.cookie.match(/_xsrf=([^;]+)/);
//   return matches ? decodeURIComponent(matches[1]) : '';
// }
function createSaveToS3Button(onSuccess) {
    return new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.saveIcon,
        tooltip: 'Push local changes to S3 backend',
        onClick: async () => {
            try {
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
                const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, 's3bridge', 'upload-s3');
                // const xsrfToken = getXsrfToken();
                const resp = await fetch(url, {
                    method: 'POST',
                    credentials: 'include',
                    // headers: {
                    //   'X-XSRFToken': xsrfToken,
                    // }, 
                });
                if (!resp.ok)
                    throw new Error(`Upload error: ${resp.status}`);
                await resp.json();
                onSuccess();
            }
            catch (err) {
                console.error('Upload failed:', err);
                alert('Upload failed: ' + err);
            }
        }
    });
}


/***/ }),

/***/ "./lib/toolbar.js":
/*!************************!*\
  !*** ./lib/toolbar.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createVersionToolbar: () => (/* binding */ createVersionToolbar)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
// File: toolbar.ts

function createVersionToolbar(dropdown) {
    const toolbar = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
    toolbar.addClass('jp-FileBrowser-version-toolbar');
    toolbar.node.style.display = 'flex';
    toolbar.node.style.alignItems = 'center';
    toolbar.node.style.padding = '2px 4px';
    toolbar.node.style.borderTop = '1px solid var(--jp-border-color2)';
    const label = document.createElement('span');
    label.textContent = 'Version:';
    label.style.margin = '0 4px';
    toolbar.node.appendChild(label);
    toolbar.node.appendChild(dropdown.node);
    return toolbar;
}


/***/ }),

/***/ "./lib/versions_dropdown.js":
/*!**********************************!*\
  !*** ./lib/versions_dropdown.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VersionsDropdownWidget: () => (/* binding */ VersionsDropdownWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__);
// File: versions_dropdown.ts




class VersionsDropdownWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        super();
        this._versionChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this.addClass('versions-dropdown-widget');
        this._select = document.createElement('select');
        this._select.style.margin = '0 4px';
        this._select.style.width = '150px';
        this._select.addEventListener('change', this._onChange.bind(this));
        this.node.appendChild(this._select);
        void this.refresh();
    }
    get versionChanged() {
        return this._versionChanged;
    }
    get selectedVersion() {
        return this._select.value;
    }
    async refresh() {
        try {
            const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServerConnection.makeSettings();
            const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, 's3bridge', 'versions');
            const response = await fetch(url, { credentials: 'include' });
            if (!response.ok)
                throw new Error(`Fetch failed: ${response.status}`);
            const result = await response.json();
            const versions = result.data.map(item => Number(item.version)).sort((a, b) => a - b);
            this._select.innerHTML = '';
            versions.forEach(v => {
                const opt = document.createElement('option');
                opt.value = v.toString();
                opt.textContent = `v${v}`;
                this._select.appendChild(opt);
            });
            if (versions.length > 0) {
                this._select.value = versions[versions.length - 1].toString();
            }
        }
        catch (err) {
            console.error('Dropdown load error:', err);
        }
    }
    async _onChange() {
        const selected = this.selectedVersion;
        try {
            const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServerConnection.makeSettings();
            const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, 's3bridge', 'versions', selected);
            const resp = await fetch(url, { method: 'PATCH', credentials: 'include' });
            if (!resp.ok)
                throw new Error(`PATCH failed: ${resp.status}`);
            await resp.json();
            this._versionChanged.emit(selected);
        }
        catch (err) {
            console.error('Version switch failed:', err);
        }
    }
    dispose() {
        this._select.removeEventListener('change', this._onChange);
        super.dispose();
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.cedf14dea7bb9ed474f0.js.map