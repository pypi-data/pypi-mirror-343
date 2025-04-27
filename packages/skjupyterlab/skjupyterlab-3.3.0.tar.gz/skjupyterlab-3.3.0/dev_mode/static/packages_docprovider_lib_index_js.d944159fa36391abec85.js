(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_docprovider_lib_index_js"],{

/***/ "../packages/docprovider/lib/awareness.js":
/*!************************************************!*\
  !*** ../packages/docprovider/lib/awareness.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "moonsOfJupyter": () => (/* binding */ moonsOfJupyter),
/* harmony export */   "getAnonymousUserName": () => (/* binding */ getAnonymousUserName),
/* harmony export */   "userColors": () => (/* binding */ userColors),
/* harmony export */   "getRandomColor": () => (/* binding */ getRandomColor)
/* harmony export */ });
// From https://en.wikipedia.org/wiki/Moons_of_Jupiter
const moonsOfJupyter = [
    'Metis',
    'Adrastea',
    'Amalthea',
    'Thebe',
    'Io',
    'Europa',
    'Ganymede',
    'Callisto',
    'Themisto',
    'Leda',
    'Ersa',
    'Pandia',
    'Himalia',
    'Lysithea',
    'Elara',
    'Dia',
    'Carpo',
    'Valetudo',
    'Euporie',
    'Eupheme',
    // 'S/2003 J 18',
    // 'S/2010 J 2',
    'Helike',
    // 'S/2003 J 16',
    // 'S/2003 J 2',
    'Euanthe',
    // 'S/2017 J 7',
    'Hermippe',
    'Praxidike',
    'Thyone',
    'Thelxinoe',
    // 'S/2017 J 3',
    'Ananke',
    'Mneme',
    // 'S/2016 J 1',
    'Orthosie',
    'Harpalyke',
    'Iocaste',
    // 'S/2017 J 9',
    // 'S/2003 J 12',
    // 'S/2003 J 4',
    'Erinome',
    'Aitne',
    'Herse',
    'Taygete',
    // 'S/2017 J 2',
    // 'S/2017 J 6',
    'Eukelade',
    'Carme',
    // 'S/2003 J 19',
    'Isonoe',
    // 'S/2003 J 10',
    'Autonoe',
    'Philophrosyne',
    'Cyllene',
    'Pasithee',
    // 'S/2010 J 1',
    'Pasiphae',
    'Sponde',
    // 'S/2017 J 8',
    'Eurydome',
    // 'S/2017 J 5',
    'Kalyke',
    'Hegemone',
    'Kale',
    'Kallichore',
    // 'S/2011 J 1',
    // 'S/2017 J 1',
    'Chaldene',
    'Arche',
    'Eirene',
    'Kore',
    // 'S/2011 J 2',
    // 'S/2003 J 9',
    'Megaclite',
    'Aoede',
    // 'S/2003 J 23',
    'Callirrhoe',
    'Sinope'
];
/**
 * Get a random user-name based on the moons of Jupyter.
 * This function returns names like "Anonymous Io" or "Anonymous Metis".
 */
const getAnonymousUserName = () => 'Anonymous ' +
    moonsOfJupyter[Math.floor(Math.random() * moonsOfJupyter.length)];
const userColors = [
    '#12A0D3',
    '#17AB30',
    '#CC8500',
    '#A79011',
    '#ee6352',
    '#609DA9',
    '#4BA749',
    '#00A1B3'
];
const getRandomColor = () => userColors[Math.floor(Math.random() * userColors.length)];


/***/ }),

/***/ "../packages/docprovider/lib/index.js":
/*!********************************************!*\
  !*** ../packages/docprovider/lib/index.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getAnonymousUserName": () => (/* reexport safe */ _awareness__WEBPACK_IMPORTED_MODULE_0__.getAnonymousUserName),
/* harmony export */   "getRandomColor": () => (/* reexport safe */ _awareness__WEBPACK_IMPORTED_MODULE_0__.getRandomColor),
/* harmony export */   "moonsOfJupyter": () => (/* reexport safe */ _awareness__WEBPACK_IMPORTED_MODULE_0__.moonsOfJupyter),
/* harmony export */   "userColors": () => (/* reexport safe */ _awareness__WEBPACK_IMPORTED_MODULE_0__.userColors),
/* harmony export */   "ProviderMock": () => (/* reexport safe */ _mock__WEBPACK_IMPORTED_MODULE_1__.ProviderMock),
/* harmony export */   "IDocumentProviderFactory": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_2__.IDocumentProviderFactory),
/* harmony export */   "WebSocketProviderWithLocks": () => (/* reexport safe */ _yprovider__WEBPACK_IMPORTED_MODULE_3__.WebSocketProviderWithLocks)
/* harmony export */ });
/* harmony import */ var _awareness__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./awareness */ "../packages/docprovider/lib/awareness.js");
/* harmony import */ var _mock__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./mock */ "../packages/docprovider/lib/mock.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./tokens */ "../packages/docprovider/lib/tokens.js");
/* harmony import */ var _yprovider__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./yprovider */ "../packages/docprovider/lib/yprovider.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module docprovider
 */






/***/ }),

/***/ "../packages/docprovider/lib/mock.js":
/*!*******************************************!*\
  !*** ../packages/docprovider/lib/mock.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ProviderMock": () => (/* binding */ ProviderMock)
/* harmony export */ });
class ProviderMock {
    requestInitialContent() {
        return Promise.resolve(false);
    }
    putInitializedState() {
        /* nop */
    }
    acquireLock() {
        return Promise.resolve(0);
    }
    releaseLock(lock) {
        /* nop */
    }
    destroy() {
        /* nop */
    }
    setPath(path) {
        /* nop */
    }
}


/***/ }),

/***/ "../packages/docprovider/lib/tokens.js":
/*!*********************************************!*\
  !*** ../packages/docprovider/lib/tokens.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IDocumentProviderFactory": () => (/* binding */ IDocumentProviderFactory)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The default document provider token.
 */
const IDocumentProviderFactory = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/docprovider:IDocumentProviderFactory');


/***/ }),

/***/ "../packages/docprovider/lib/yprovider.js":
/*!************************************************!*\
  !*** ../packages/docprovider/lib/yprovider.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "WebSocketProviderWithLocks": () => (/* binding */ WebSocketProviderWithLocks)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var lib0_decoding__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! lib0/decoding */ "../node_modules/lib0/decoding.js");
/* harmony import */ var lib0_encoding__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! lib0/encoding */ "../node_modules/lib0/encoding.js");
/* harmony import */ var y_websocket__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! y-websocket */ "../node_modules/y-websocket/src/y-websocket.js");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! yjs */ "webpack/sharing/consume/default/yjs/yjs");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(yjs__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _awareness__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./awareness */ "../packages/docprovider/lib/awareness.js");
/* harmony import */ var lib0_environment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! lib0/environment */ "../node_modules/lib0/environment.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/







/**
 * A class to provide Yjs synchronization over WebSocket.
 *
 * The user can specify their own user-name and user-color by adding url parameters:
 *   ?username=Alice&usercolor=007007
 * where usercolor must be a six-digit hexadecimal encoded RGB value without the hash token.
 *
 * We specify custom messages that the server can interpret. For reference please look in yjs_ws_server.
 *
 */
class WebSocketProviderWithLocks extends y_websocket__WEBPACK_IMPORTED_MODULE_2__.WebsocketProvider {
    /**
     * Construct a new WebSocketProviderWithLocks
     *
     * @param options The instantiation options for a WebSocketProviderWithLocks
     */
    constructor(options) {
        var _a;
        super(options.url, options.contentType + ':' + options.path, options.ymodel.ydoc, {
            awareness: options.ymodel.awareness
        });
        this._currentLockRequest = null;
        this._initialContentRequest = null;
        this._path = options.path;
        this._contentType = options.contentType;
        this._serverUrl = options.url;
        const color = '#' + lib0_environment__WEBPACK_IMPORTED_MODULE_3__.getParam('--usercolor', (0,_awareness__WEBPACK_IMPORTED_MODULE_4__.getRandomColor)().slice(1));
        const name = decodeURIComponent(lib0_environment__WEBPACK_IMPORTED_MODULE_3__.getParam('--username', (0,_awareness__WEBPACK_IMPORTED_MODULE_4__.getAnonymousUserName)()));
        const awareness = options.ymodel.awareness;
        const currState = awareness.getLocalState();
        // only set if this was not already set by another plugin
        if (currState && ((_a = currState.user) === null || _a === void 0 ? void 0 : _a.name) == null) {
            options.ymodel.awareness.setLocalStateField('user', {
                name,
                color
            });
        }
        // Message handler that confirms when a lock has been acquired
        this.messageHandlers[127] = (encoder, decoder, provider, emitSynced, messageType) => {
            // acquired lock
            const timestamp = lib0_decoding__WEBPACK_IMPORTED_MODULE_5__.readUint32(decoder);
            const lockRequest = this._currentLockRequest;
            this._currentLockRequest = null;
            if (lockRequest) {
                lockRequest.resolve(timestamp);
            }
        };
        // Message handler that receives the initial content
        this.messageHandlers[125] = (encoder, decoder, provider, emitSynced, messageType) => {
            // received initial content
            const initialContent = lib0_decoding__WEBPACK_IMPORTED_MODULE_5__.readTailAsUint8Array(decoder);
            // Apply data from server
            if (initialContent.byteLength > 0) {
                setTimeout(() => {
                    yjs__WEBPACK_IMPORTED_MODULE_1__.applyUpdate(this.doc, initialContent);
                }, 0);
            }
            const initialContentRequest = this._initialContentRequest;
            this._initialContentRequest = null;
            if (initialContentRequest) {
                initialContentRequest.resolve(initialContent.byteLength > 0);
            }
        };
        this._isInitialized = false;
        this._onConnectionStatus = this._onConnectionStatus.bind(this);
        this.on('status', this._onConnectionStatus);
    }
    setPath(newPath) {
        if (newPath !== this._path) {
            this._path = newPath;
            const encoder = lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.createEncoder();
            lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.write(encoder, 123);
            // writing a utf8 string to the encoder
            const escapedPath = unescape(encodeURIComponent(this._contentType + ':' + newPath));
            for (let i = 0; i < escapedPath.length; i++) {
                lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.write(encoder, 
                /** @type {number} */ escapedPath.codePointAt(i));
            }
            this._sendMessage(lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.toUint8Array(encoder));
            // prevent publishing messages to the old channel id.
            this.disconnectBc();
            // The next time the provider connects, we should connect through a different server url
            this.bcChannel =
                this._serverUrl + '/' + this._contentType + ':' + this._path;
            this.url = this.bcChannel;
            this.connectBc();
        }
    }
    /**
     * Resolves to true if the initial content has been initialized on the server. false otherwise.
     */
    requestInitialContent() {
        if (this._initialContentRequest) {
            return this._initialContentRequest.promise;
        }
        this._initialContentRequest = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        this._sendMessage(new Uint8Array([125]));
        // Resolve with true if the server doesn't respond for some reason.
        // In case of a connection problem, we don't want the user to re-initialize the window.
        // Instead wait for y-websocket to connect to the server.
        // @todo maybe we should reload instead..
        setTimeout(() => { var _a; return (_a = this._initialContentRequest) === null || _a === void 0 ? void 0 : _a.resolve(false); }, 1000);
        return this._initialContentRequest.promise;
    }
    /**
     * Put the initialized state.
     */
    putInitializedState() {
        const encoder = lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.createEncoder();
        lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.writeVarUint(encoder, 124);
        lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.writeUint8Array(encoder, yjs__WEBPACK_IMPORTED_MODULE_1__.encodeStateAsUpdate(this.doc));
        this._sendMessage(lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.toUint8Array(encoder));
        this._isInitialized = true;
    }
    /**
     * Acquire a lock.
     * Returns a Promise that resolves to the lock number.
     */
    acquireLock() {
        if (this._currentLockRequest) {
            return this._currentLockRequest.promise;
        }
        this._sendMessage(new Uint8Array([127]));
        // try to acquire lock in regular interval
        if (this._requestLockInterval) {
            clearInterval(this._requestLockInterval);
        }
        this._requestLockInterval = setInterval(() => {
            if (this.wsconnected) {
                // try to acquire lock
                this._sendMessage(new Uint8Array([127]));
            }
        }, 500);
        let resolve, reject;
        const promise = new Promise((_resolve, _reject) => {
            resolve = _resolve;
            reject = _reject;
        });
        this._currentLockRequest = { promise, resolve, reject };
        return promise;
    }
    /**
     * Release a lock.
     *
     * @param lock The lock to release.
     */
    releaseLock(lock) {
        const encoder = lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.createEncoder();
        // reply with release lock
        lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.writeVarUint(encoder, 126);
        lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.writeUint32(encoder, lock);
        // releasing lock
        this._sendMessage(lib0_encoding__WEBPACK_IMPORTED_MODULE_6__.toUint8Array(encoder));
        if (this._requestLockInterval) {
            clearInterval(this._requestLockInterval);
        }
    }
    /**
     * Send a new message to WebSocket server.
     *
     * @param message The message to send
     */
    _sendMessage(message) {
        // send once connected
        const send = () => {
            setTimeout(() => {
                if (this.wsconnected) {
                    this.ws.send(message);
                }
                else {
                    this.once('status', send);
                }
            }, 0);
        };
        send();
    }
    /**
     * Handle a change to the connection status.
     *
     * @param status The connection status.
     */
    async _onConnectionStatus(status) {
        if (this._isInitialized && status.status === 'connected') {
            const lock = await this.acquireLock();
            const contentIsInitialized = await this.requestInitialContent();
            if (!contentIsInitialized) {
                this.putInitializedState();
            }
            this.releaseLock(lock);
        }
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jcHJvdmlkZXIvc3JjL2F3YXJlbmVzcy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jcHJvdmlkZXIvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9kb2Nwcm92aWRlci9zcmMvbW9jay50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jcHJvdmlkZXIvc3JjL3Rva2Vucy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jcHJvdmlkZXIvc3JjL3lwcm92aWRlci50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsc0RBQXNEO0FBQy9DLE1BQU0sY0FBYyxHQUFHO0lBQzVCLE9BQU87SUFDUCxVQUFVO0lBQ1YsVUFBVTtJQUNWLE9BQU87SUFDUCxJQUFJO0lBQ0osUUFBUTtJQUNSLFVBQVU7SUFDVixVQUFVO0lBQ1YsVUFBVTtJQUNWLE1BQU07SUFDTixNQUFNO0lBQ04sUUFBUTtJQUNSLFNBQVM7SUFDVCxVQUFVO0lBQ1YsT0FBTztJQUNQLEtBQUs7SUFDTCxPQUFPO0lBQ1AsVUFBVTtJQUNWLFNBQVM7SUFDVCxTQUFTO0lBQ1QsaUJBQWlCO0lBQ2pCLGdCQUFnQjtJQUNoQixRQUFRO0lBQ1IsaUJBQWlCO0lBQ2pCLGdCQUFnQjtJQUNoQixTQUFTO0lBQ1QsZ0JBQWdCO0lBQ2hCLFVBQVU7SUFDVixXQUFXO0lBQ1gsUUFBUTtJQUNSLFdBQVc7SUFDWCxnQkFBZ0I7SUFDaEIsUUFBUTtJQUNSLE9BQU87SUFDUCxnQkFBZ0I7SUFDaEIsVUFBVTtJQUNWLFdBQVc7SUFDWCxTQUFTO0lBQ1QsZ0JB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QUFJLE1BQU0sQ0FBQyxNQUFNLEtBQUssV0FBVyxFQUFFO1lBQ3hELE1BQU0sSUFBSSxHQUFHLE1BQU0sSUFBSSxDQUFDLFdBQVcsRUFBRSxDQUFDO1lBQ3RDLE1BQU0sb0JBQW9CLEdBQUcsTUFBTSxJQUFJLENBQUMscUJBQXFCLEVBQUUsQ0FBQztZQUNoRSxJQUFJLENBQUMsb0JBQW9CLEVBQUU7Z0JBQ3pCLElBQUksQ0FBQyxtQkFBbUIsRUFBRSxDQUFDO2FBQzVCO1lBQ0QsSUFBSSxDQUFDLFdBQVcsQ0FBQyxJQUFJLENBQUMsQ0FBQztTQUN4QjtJQUNILENBQUM7Q0FhRiIsImZpbGUiOiJwYWNrYWdlc19kb2Nwcm92aWRlcl9saWJfaW5kZXhfanMuZDk0NDE1OWZhMzYzOTFhYmVjODUuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBGcm9tIGh0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy93aWtpL01vb25zX29mX0p1cGl0ZXJcbmV4cG9ydCBjb25zdCBtb29uc09mSnVweXRlciA9IFtcbiAgJ01ldGlzJyxcbiAgJ0FkcmFzdGVhJyxcbiAgJ0FtYWx0aGVhJyxcbiAgJ1RoZWJlJyxcbiAgJ0lvJyxcbiAgJ0V1cm9wYScsXG4gICdHYW55bWVkZScsXG4gICdDYWxsaXN0bycsXG4gICdUaGVtaXN0bycsXG4gICdMZWRhJyxcbiAgJ0Vyc2EnLFxuICAnUGFuZGlhJyxcbiAgJ0hpbWFsaWEnLFxuICAnTHlzaXRoZWEnLFxuICAnRWxhcmEnLFxuICAnRGlhJyxcbiAgJ0NhcnBvJyxcbiAgJ1ZhbGV0dWRvJyxcbiAgJ0V1cG9yaWUnLFxuICAnRXVwaGVtZScsXG4gIC8vICdTLzIwMDMgSiAxOCcsXG4gIC8vICdTLzIwMTAgSiAyJyxcbiAgJ0hlbGlrZScsXG4gIC8vICdTLzIwMDMgSiAxNicsXG4gIC8vICdTLzIwMDMgSiAyJyxcbiAgJ0V1YW50aGUnLFxuICAvLyAnUy8yMDE3IEogNycsXG4gICdIZXJtaXBwZScsXG4gICdQcmF4aWRpa2UnLFxuICAnVGh5b25lJyxcbiAgJ1RoZWx4aW5vZScsXG4gIC8vICdTLzIwMTcgSiAzJyxcbiAgJ0FuYW5rZScsXG4gICdNbmVtZScsXG4gIC8vICdTLzIwMTYgSiAxJyxcbiAgJ09ydGhvc2llJyxcbiAgJ0hhcnBhbHlrZScsXG4gICdJb2Nhc3RlJyxcbiAgLy8gJ1MvMjAxNyBKIDknLFxuICAvLyAnUy8yMDAzIEogMTInLFxuICAvLyAnUy8yMDAzIEogNCcsXG4gICdFcmlub21lJyxcbiAgJ0FpdG5lJyxcbiAgJ0hlcnNlJyxcbiAgJ1RheWdldGUnLFxuICAvLyAnUy8yMDE3IEogMicsXG4gIC8vICdTLzIwMTcgSiA2JyxcbiAgJ0V1a2VsYWRlJyxcbiAgJ0Nhcm1lJyxcbiAgLy8gJ1MvMjAwMyBKIDE5JyxcbiAgJ0lzb25vZScsXG4gIC8vICdTLzIwMDMgSiAxMCcsXG4gICdBdXRvbm9lJyxcbiAgJ1BoaWxvcGhyb3N5bmUnLFxuICAnQ3lsbGVuZScsXG4gICdQYXNpdGhlZScsXG4gIC8vICdTLzIwMTAgSiAxJyxcbiAgJ1Bhc2lwaGFlJyxcbiAgJ1Nwb25kZScsXG4gIC8vICdTLzIwMTcgSiA4JyxcbiAgJ0V1cnlkb21lJyxcbiAgLy8gJ1MvMjAxNyBKIDUnLFxuICAnS2FseWtlJyxcbiAgJ0hlZ2Vtb25lJyxcbiAgJ0thbGUnLFxuICAnS2FsbGljaG9yZScsXG4gIC8vICdTLzIwMTEgSiAxJyxcbiAgLy8gJ1MvMjAxNyBKIDEnLFxuICAnQ2hhbGRlbmUnLFxuICAnQXJjaGUnLFxuICAnRWlyZW5lJyxcbiAgJ0tvcmUnLFxuICAvLyAnUy8yMDExIEogMicsXG4gIC8vICdTLzIwMDMgSiA5JyxcbiAgJ01lZ2FjbGl0ZScsXG4gICdBb2VkZScsXG4gIC8vICdTLzIwMDMgSiAyMycsXG4gICdDYWxsaXJyaG9lJyxcbiAgJ1Npbm9wZSdcbl07XG5cbi8qKlxuICogR2V0IGEgcmFuZG9tIHVzZXItbmFtZSBiYXNlZCBvbiB0aGUgbW9vbnMgb2YgSnVweXRlci5cbiAqIFRoaXMgZnVuY3Rpb24gcmV0dXJucyBuYW1lcyBsaWtlIFwiQW5vbnltb3VzIElvXCIgb3IgXCJBbm9ueW1vdXMgTWV0aXNcIi5cbiAqL1xuZXhwb3J0IGNvbnN0IGdldEFub255bW91c1VzZXJOYW1lID0gKCk6IHN0cmluZyA9PlxuICAnQW5vbnltb3VzICcgK1xuICBtb29uc09mSnVweXRlcltNYXRoLmZsb29yKE1hdGgucmFuZG9tKCkgKiBtb29uc09mSnVweXRlci5sZW5ndGgpXTtcblxuZXhwb3J0IGNvbnN0IHVzZXJDb2xvcnMgPSBbXG4gICcjMTJBMEQzJyxcbiAgJyMxN0FCMzAnLFxuICAnI0NDODUwMCcsXG4gICcjQTc5MDExJyxcbiAgJyNlZTYzNTInLFxuICAnIzYwOURBOScsXG4gICcjNEJBNzQ5JyxcbiAgJyMwMEExQjMnXG5dO1xuXG5leHBvcnQgY29uc3QgZ2V0UmFuZG9tQ29sb3IgPSAoKTogc3RyaW5nID0+XG4gIHVzZXJDb2xvcnNbTWF0aC5mbG9vcihNYXRoLnJhbmRvbSgpICogdXNlckNvbG9ycy5sZW5ndGgpXTtcbiIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgZG9jcHJvdmlkZXJcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL2F3YXJlbmVzcyc7XG5leHBvcnQgKiBmcm9tICcuL21vY2snO1xuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuZXhwb3J0ICogZnJvbSAnLi95cHJvdmlkZXInO1xuIiwiaW1wb3J0IHsgSURvY3VtZW50UHJvdmlkZXIgfSBmcm9tICcuL2luZGV4JztcblxuZXhwb3J0IGNsYXNzIFByb3ZpZGVyTW9jayBpbXBsZW1lbnRzIElEb2N1bWVudFByb3ZpZGVyIHtcbiAgcmVxdWVzdEluaXRpYWxDb250ZW50KCk6IFByb21pc2U8Ym9vbGVhbj4ge1xuICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUoZmFsc2UpO1xuICB9XG4gIHB1dEluaXRpYWxpemVkU3RhdGUoKTogdm9pZCB7XG4gICAgLyogbm9wICovXG4gIH1cbiAgYWNxdWlyZUxvY2soKTogUHJvbWlzZTxudW1iZXI+IHtcbiAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKDApO1xuICB9XG4gIHJlbGVhc2VMb2NrKGxvY2s6IG51bWJlcik6IHZvaWQge1xuICAgIC8qIG5vcCAqL1xuICB9XG4gIGRlc3Ryb3koKTogdm9pZCB7XG4gICAgLyogbm9wICovXG4gIH1cbiAgc2V0UGF0aChwYXRoOiBzdHJpbmcpOiB2b2lkIHtcbiAgICAvKiBub3AgKi9cbiAgfVxufVxuIiwiaW1wb3J0IHsgRG9jdW1lbnRDaGFuZ2UsIFlEb2N1bWVudCB9IGZyb20gJ0BqdXB5dGVybGFiL3NoYXJlZC1tb2RlbHMnO1xuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgZG9jdW1lbnQgcHJvdmlkZXIgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJRG9jdW1lbnRQcm92aWRlckZhY3RvcnkgPSBuZXcgVG9rZW48SURvY3VtZW50UHJvdmlkZXJGYWN0b3J5PihcbiAgJ0BqdXB5dGVybGFiL2RvY3Byb3ZpZGVyOklEb2N1bWVudFByb3ZpZGVyRmFjdG9yeSdcbik7XG5cbi8qKlxuICogQW4gaW50ZXJmYWNlIGZvciBhIGRvY3VtZW50IHByb3ZpZGVyLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElEb2N1bWVudFByb3ZpZGVyIHtcbiAgLyoqXG4gICAqIFJlc29sdmVzIHRvIHRydWUgaWYgdGhlIGluaXRpYWwgY29udGVudCBoYXMgYmVlbiBpbml0aWFsaXplZCBvbiB0aGUgc2VydmVyLiBmYWxzZSBvdGhlcndpc2UuXG4gICAqL1xuICByZXF1ZXN0SW5pdGlhbENvbnRlbnQoKTogUHJvbWlzZTxib29sZWFuPjtcblxuICAvKipcbiAgICogUHV0IHRoZSBpbml0aWFsaXplZCBzdGF0ZS5cbiAgICovXG4gIHB1dEluaXRpYWxpemVkU3RhdGUoKTogdm9pZDtcblxuICAvKipcbiAgICogQWNxdWlyZSBhIGxvY2suXG4gICAqIFJldHVybnMgYSBQcm9taXNlIHRoYXQgcmVzb2x2ZXMgdG8gdGhlIGxvY2sgbnVtYmVyLlxuICAgKi9cbiAgYWNxdWlyZUxvY2soKTogUHJvbWlzZTxudW1iZXI+O1xuXG4gIC8qKlxuICAgKiBSZWxlYXNlIGEgbG9jay5cbiAgICpcbiAgICogQHBhcmFtIGxvY2sgVGhlIGxvY2sgdG8gcmVsZWFzZS5cbiAgICovXG4gIHJlbGVhc2VMb2NrKGxvY2s6IG51bWJlcik6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIFRoaXMgc2hvdWxkIGJlIGNhbGxlZCBieSB0aGUgZG9jcmVnaXN0cnkgd2hlbiB0aGUgZmlsZSBoYXMgYmVlbiByZW5hbWVkIHRvIHVwZGF0ZSB0aGUgd2Vic29ja2V0IGNvbm5lY3Rpb24gdXJsXG4gICAqL1xuICBzZXRQYXRoKG5ld1BhdGg6IHN0cmluZyk6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIERlc3Ryb3kgdGhlIHByb3ZpZGVyLlxuICAgKi9cbiAgZGVzdHJveSgpOiB2b2lkO1xufVxuXG4vKipcbiAqIFRoZSB0eXBlIGZvciB0aGUgZG9jdW1lbnQgcHJvdmlkZXIgZmFjdG9yeS5cbiAqL1xuZXhwb3J0IHR5cGUgSURvY3VtZW50UHJvdmlkZXJGYWN0b3J5ID0gKFxuICBvcHRpb25zOiBJRG9jdW1lbnRQcm92aWRlckZhY3RvcnkuSU9wdGlvbnNcbikgPT4gSURvY3VtZW50UHJvdmlkZXI7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIElEb2N1bWVudFByb3ZpZGVyRmFjdG9yeSBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElEb2N1bWVudFByb3ZpZGVyRmFjdG9yeSB7XG4gIC8qKlxuICAgKiBUaGUgaW5zdGFudGlhdGlvbiBvcHRpb25zIGZvciBhIElEb2N1bWVudFByb3ZpZGVyRmFjdG9yeS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBuYW1lIChpZCkgb2YgdGhlIHJvb21cbiAgICAgKi9cbiAgICBwYXRoOiBzdHJpbmc7XG4gICAgY29udGVudFR5cGU6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBZTm90ZWJvb2suXG4gICAgICovXG4gICAgeW1vZGVsOiBZRG9jdW1lbnQ8RG9jdW1lbnRDaGFuZ2U+O1xuICB9XG59XG4iLCIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cblxuaW1wb3J0IHsgUHJvbWlzZURlbGVnYXRlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0ICogYXMgZGVjb2RpbmcgZnJvbSAnbGliMC9kZWNvZGluZyc7XG5pbXBvcnQgKiBhcyBlbmNvZGluZyBmcm9tICdsaWIwL2VuY29kaW5nJztcbmltcG9ydCB7IFdlYnNvY2tldFByb3ZpZGVyIH0gZnJvbSAneS13ZWJzb2NrZXQnO1xuaW1wb3J0ICogYXMgWSBmcm9tICd5anMnO1xuaW1wb3J0IHsgSURvY3VtZW50UHJvdmlkZXIsIElEb2N1bWVudFByb3ZpZGVyRmFjdG9yeSB9IGZyb20gJy4vdG9rZW5zJztcbmltcG9ydCB7IGdldEFub255bW91c1VzZXJOYW1lLCBnZXRSYW5kb21Db2xvciB9IGZyb20gJy4vYXdhcmVuZXNzJztcbmltcG9ydCAqIGFzIGVudiBmcm9tICdsaWIwL2Vudmlyb25tZW50JztcblxuLyoqXG4gKiBBIGNsYXNzIHRvIHByb3ZpZGUgWWpzIHN5bmNocm9uaXphdGlvbiBvdmVyIFdlYlNvY2tldC5cbiAqXG4gKiBUaGUgdXNlciBjYW4gc3BlY2lmeSB0aGVpciBvd24gdXNlci1uYW1lIGFuZCB1c2VyLWNvbG9yIGJ5IGFkZGluZyB1cmwgcGFyYW1ldGVyczpcbiAqICAgP3VzZXJuYW1lPUFsaWNlJnVzZXJjb2xvcj0wMDcwMDdcbiAqIHdoZXJlIHVzZXJjb2xvciBtdXN0IGJlIGEgc2l4LWRpZ2l0IGhleGFkZWNpbWFsIGVuY29kZWQgUkdCIHZhbHVlIHdpdGhvdXQgdGhlIGhhc2ggdG9rZW4uXG4gKlxuICogV2Ugc3BlY2lmeSBjdXN0b20gbWVzc2FnZXMgdGhhdCB0aGUgc2VydmVyIGNhbiBpbnRlcnByZXQuIEZvciByZWZlcmVuY2UgcGxlYXNlIGxvb2sgaW4geWpzX3dzX3NlcnZlci5cbiAqXG4gKi9cbmV4cG9ydCBjbGFzcyBXZWJTb2NrZXRQcm92aWRlcldpdGhMb2Nrc1xuICBleHRlbmRzIFdlYnNvY2tldFByb3ZpZGVyXG4gIGltcGxlbWVudHMgSURvY3VtZW50UHJvdmlkZXIge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IFdlYlNvY2tldFByb3ZpZGVyV2l0aExvY2tzXG4gICAqXG4gICAqIEBwYXJhbSBvcHRpb25zIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGEgV2ViU29ja2V0UHJvdmlkZXJXaXRoTG9ja3NcbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IFdlYlNvY2tldFByb3ZpZGVyV2l0aExvY2tzLklPcHRpb25zKSB7XG4gICAgc3VwZXIoXG4gICAgICBvcHRpb25zLnVybCxcbiAgICAgIG9wdGlvbnMuY29udGVudFR5cGUgKyAnOicgKyBvcHRpb25zLnBhdGgsXG4gICAgICBvcHRpb25zLnltb2RlbC55ZG9jLFxuICAgICAge1xuICAgICAgICBhd2FyZW5lc3M6IG9wdGlvbnMueW1vZGVsLmF3YXJlbmVzc1xuICAgICAgfVxuICAgICk7XG4gICAgdGhpcy5fcGF0aCA9IG9wdGlvbnMucGF0aDtcbiAgICB0aGlzLl9jb250ZW50VHlwZSA9IG9wdGlvbnMuY29udGVudFR5cGU7XG4gICAgdGhpcy5fc2VydmVyVXJsID0gb3B0aW9ucy51cmw7XG4gICAgY29uc3QgY29sb3IgPSAnIycgKyBlbnYuZ2V0UGFyYW0oJy0tdXNlcmNvbG9yJywgZ2V0UmFuZG9tQ29sb3IoKS5zbGljZSgxKSk7XG4gICAgY29uc3QgbmFtZSA9IGRlY29kZVVSSUNvbXBvbmVudChcbiAgICAgIGVudi5nZXRQYXJhbSgnLS11c2VybmFtZScsIGdldEFub255bW91c1VzZXJOYW1lKCkpXG4gICAgKTtcbiAgICBjb25zdCBhd2FyZW5lc3MgPSBvcHRpb25zLnltb2RlbC5hd2FyZW5lc3M7XG4gICAgY29uc3QgY3VyclN0YXRlID0gYXdhcmVuZXNzLmdldExvY2FsU3RhdGUoKTtcbiAgICAvLyBvbmx5IHNldCBpZiB0aGlzIHdhcyBub3QgYWxyZWFkeSBzZXQgYnkgYW5vdGhlciBwbHVnaW5cbiAgICBpZiAoY3VyclN0YXRlICYmIGN1cnJTdGF0ZS51c2VyPy5uYW1lID09IG51bGwpIHtcbiAgICAgIG9wdGlvbnMueW1vZGVsLmF3YXJlbmVzcy5zZXRMb2NhbFN0YXRlRmllbGQoJ3VzZXInLCB7XG4gICAgICAgIG5hbWUsXG4gICAgICAgIGNvbG9yXG4gICAgICB9KTtcbiAgICB9XG5cbiAgICAvLyBNZXNzYWdlIGhhbmRsZXIgdGhhdCBjb25maXJtcyB3aGVuIGEgbG9jayBoYXMgYmVlbiBhY3F1aXJlZFxuICAgIHRoaXMubWVzc2FnZUhhbmRsZXJzWzEyN10gPSAoXG4gICAgICBlbmNvZGVyLFxuICAgICAgZGVjb2RlcixcbiAgICAgIHByb3ZpZGVyLFxuICAgICAgZW1pdFN5bmNlZCxcbiAgICAgIG1lc3NhZ2VUeXBlXG4gICAgKSA9PiB7XG4gICAgICAvLyBhY3F1aXJlZCBsb2NrXG4gICAgICBjb25zdCB0aW1lc3RhbXAgPSBkZWNvZGluZy5yZWFkVWludDMyKGRlY29kZXIpO1xuICAgICAgY29uc3QgbG9ja1JlcXVlc3QgPSB0aGlzLl9jdXJyZW50TG9ja1JlcXVlc3Q7XG4gICAgICB0aGlzLl9jdXJyZW50TG9ja1JlcXVlc3QgPSBudWxsO1xuICAgICAgaWYgKGxvY2tSZXF1ZXN0KSB7XG4gICAgICAgIGxvY2tSZXF1ZXN0LnJlc29sdmUodGltZXN0YW1wKTtcbiAgICAgIH1cbiAgICB9O1xuICAgIC8vIE1lc3NhZ2UgaGFuZGxlciB0aGF0IHJlY2VpdmVzIHRoZSBpbml0aWFsIGNvbnRlbnRcbiAgICB0aGlzLm1lc3NhZ2VIYW5kbGVyc1sxMjVdID0gKFxuICAgICAgZW5jb2RlcixcbiAgICAgIGRlY29kZXIsXG4gICAgICBwcm92aWRlcixcbiAgICAgIGVtaXRTeW5jZWQsXG4gICAgICBtZXNzYWdlVHlwZVxuICAgICkgPT4ge1xuICAgICAgLy8gcmVjZWl2ZWQgaW5pdGlhbCBjb250ZW50XG4gICAgICBjb25zdCBpbml0aWFsQ29udGVudCA9IGRlY29kaW5nLnJlYWRUYWlsQXNVaW50OEFycmF5KGRlY29kZXIpO1xuICAgICAgLy8gQXBwbHkgZGF0YSBmcm9tIHNlcnZlclxuICAgICAgaWYgKGluaXRpYWxDb250ZW50LmJ5dGVMZW5ndGggPiAwKSB7XG4gICAgICAgIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgICAgIFkuYXBwbHlVcGRhdGUodGhpcy5kb2MsIGluaXRpYWxDb250ZW50KTtcbiAgICAgICAgfSwgMCk7XG4gICAgICB9XG4gICAgICBjb25zdCBpbml0aWFsQ29udGVudFJlcXVlc3QgPSB0aGlzLl9pbml0aWFsQ29udGVudFJlcXVlc3Q7XG4gICAgICB0aGlzLl9pbml0aWFsQ29udGVudFJlcXVlc3QgPSBudWxsO1xuICAgICAgaWYgKGluaXRpYWxDb250ZW50UmVxdWVzdCkge1xuICAgICAgICBpbml0aWFsQ29udGVudFJlcXVlc3QucmVzb2x2ZShpbml0aWFsQ29udGVudC5ieXRlTGVuZ3RoID4gMCk7XG4gICAgICB9XG4gICAgfTtcbiAgICB0aGlzLl9pc0luaXRpYWxpemVkID0gZmFsc2U7XG4gICAgdGhpcy5fb25Db25uZWN0aW9uU3RhdHVzID0gdGhpcy5fb25Db25uZWN0aW9uU3RhdHVzLmJpbmQodGhpcyk7XG4gICAgdGhpcy5vbignc3RhdHVzJywgdGhpcy5fb25Db25uZWN0aW9uU3RhdHVzKTtcbiAgfVxuXG4gIHNldFBhdGgobmV3UGF0aDogc3RyaW5nKTogdm9pZCB7XG4gICAgaWYgKG5ld1BhdGggIT09IHRoaXMuX3BhdGgpIHtcbiAgICAgIHRoaXMuX3BhdGggPSBuZXdQYXRoO1xuICAgICAgY29uc3QgZW5jb2RlciA9IGVuY29kaW5nLmNyZWF0ZUVuY29kZXIoKTtcbiAgICAgIGVuY29kaW5nLndyaXRlKGVuY29kZXIsIDEyMyk7XG4gICAgICAvLyB3cml0aW5nIGEgdXRmOCBzdHJpbmcgdG8gdGhlIGVuY29kZXJcbiAgICAgIGNvbnN0IGVzY2FwZWRQYXRoID0gdW5lc2NhcGUoXG4gICAgICAgIGVuY29kZVVSSUNvbXBvbmVudCh0aGlzLl9jb250ZW50VHlwZSArICc6JyArIG5ld1BhdGgpXG4gICAgICApO1xuICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCBlc2NhcGVkUGF0aC5sZW5ndGg7IGkrKykge1xuICAgICAgICBlbmNvZGluZy53cml0ZShcbiAgICAgICAgICBlbmNvZGVyLFxuICAgICAgICAgIC8qKiBAdHlwZSB7bnVtYmVyfSAqLyBlc2NhcGVkUGF0aC5jb2RlUG9pbnRBdChpKSFcbiAgICAgICAgKTtcbiAgICAgIH1cbiAgICAgIHRoaXMuX3NlbmRNZXNzYWdlKGVuY29kaW5nLnRvVWludDhBcnJheShlbmNvZGVyKSk7XG4gICAgICAvLyBwcmV2ZW50IHB1Ymxpc2hpbmcgbWVzc2FnZXMgdG8gdGhlIG9sZCBjaGFubmVsIGlkLlxuICAgICAgdGhpcy5kaXNjb25uZWN0QmMoKTtcbiAgICAgIC8vIFRoZSBuZXh0IHRpbWUgdGhlIHByb3ZpZGVyIGNvbm5lY3RzLCB3ZSBzaG91bGQgY29ubmVjdCB0aHJvdWdoIGEgZGlmZmVyZW50IHNlcnZlciB1cmxcbiAgICAgIHRoaXMuYmNDaGFubmVsID1cbiAgICAgICAgdGhpcy5fc2VydmVyVXJsICsgJy8nICsgdGhpcy5fY29udGVudFR5cGUgKyAnOicgKyB0aGlzLl9wYXRoO1xuICAgICAgdGhpcy51cmwgPSB0aGlzLmJjQ2hhbm5lbDtcbiAgICAgIHRoaXMuY29ubmVjdEJjKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFJlc29sdmVzIHRvIHRydWUgaWYgdGhlIGluaXRpYWwgY29udGVudCBoYXMgYmVlbiBpbml0aWFsaXplZCBvbiB0aGUgc2VydmVyLiBmYWxzZSBvdGhlcndpc2UuXG4gICAqL1xuICByZXF1ZXN0SW5pdGlhbENvbnRlbnQoKTogUHJvbWlzZTxib29sZWFuPiB7XG4gICAgaWYgKHRoaXMuX2luaXRpYWxDb250ZW50UmVxdWVzdCkge1xuICAgICAgcmV0dXJuIHRoaXMuX2luaXRpYWxDb250ZW50UmVxdWVzdC5wcm9taXNlO1xuICAgIH1cblxuICAgIHRoaXMuX2luaXRpYWxDb250ZW50UmVxdWVzdCA9IG5ldyBQcm9taXNlRGVsZWdhdGU8Ym9vbGVhbj4oKTtcbiAgICB0aGlzLl9zZW5kTWVzc2FnZShuZXcgVWludDhBcnJheShbMTI1XSkpO1xuXG4gICAgLy8gUmVzb2x2ZSB3aXRoIHRydWUgaWYgdGhlIHNlcnZlciBkb2Vzbid0IHJlc3BvbmQgZm9yIHNvbWUgcmVhc29uLlxuICAgIC8vIEluIGNhc2Ugb2YgYSBjb25uZWN0aW9uIHByb2JsZW0sIHdlIGRvbid0IHdhbnQgdGhlIHVzZXIgdG8gcmUtaW5pdGlhbGl6ZSB0aGUgd2luZG93LlxuICAgIC8vIEluc3RlYWQgd2FpdCBmb3IgeS13ZWJzb2NrZXQgdG8gY29ubmVjdCB0byB0aGUgc2VydmVyLlxuICAgIC8vIEB0b2RvIG1heWJlIHdlIHNob3VsZCByZWxvYWQgaW5zdGVhZC4uXG4gICAgc2V0VGltZW91dCgoKSA9PiB0aGlzLl9pbml0aWFsQ29udGVudFJlcXVlc3Q/LnJlc29sdmUoZmFsc2UpLCAxMDAwKTtcbiAgICByZXR1cm4gdGhpcy5faW5pdGlhbENvbnRlbnRSZXF1ZXN0LnByb21pc2U7XG4gIH1cblxuICAvKipcbiAgICogUHV0IHRoZSBpbml0aWFsaXplZCBzdGF0ZS5cbiAgICovXG4gIHB1dEluaXRpYWxpemVkU3RhdGUoKTogdm9pZCB7XG4gICAgY29uc3QgZW5jb2RlciA9IGVuY29kaW5nLmNyZWF0ZUVuY29kZXIoKTtcbiAgICBlbmNvZGluZy53cml0ZVZhclVpbnQoZW5jb2RlciwgMTI0KTtcbiAgICBlbmNvZGluZy53cml0ZVVpbnQ4QXJyYXkoZW5jb2RlciwgWS5lbmNvZGVTdGF0ZUFzVXBkYXRlKHRoaXMuZG9jKSk7XG4gICAgdGhpcy5fc2VuZE1lc3NhZ2UoZW5jb2RpbmcudG9VaW50OEFycmF5KGVuY29kZXIpKTtcbiAgICB0aGlzLl9pc0luaXRpYWxpemVkID0gdHJ1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBY3F1aXJlIGEgbG9jay5cbiAgICogUmV0dXJucyBhIFByb21pc2UgdGhhdCByZXNvbHZlcyB0byB0aGUgbG9jayBudW1iZXIuXG4gICAqL1xuICBhY3F1aXJlTG9jaygpOiBQcm9taXNlPG51bWJlcj4ge1xuICAgIGlmICh0aGlzLl9jdXJyZW50TG9ja1JlcXVlc3QpIHtcbiAgICAgIHJldHVybiB0aGlzLl9jdXJyZW50TG9ja1JlcXVlc3QucHJvbWlzZTtcbiAgICB9XG4gICAgdGhpcy5fc2VuZE1lc3NhZ2UobmV3IFVpbnQ4QXJyYXkoWzEyN10pKTtcbiAgICAvLyB0cnkgdG8gYWNxdWlyZSBsb2NrIGluIHJlZ3VsYXIgaW50ZXJ2YWxcbiAgICBpZiAodGhpcy5fcmVxdWVzdExvY2tJbnRlcnZhbCkge1xuICAgICAgY2xlYXJJbnRlcnZhbCh0aGlzLl9yZXF1ZXN0TG9ja0ludGVydmFsKTtcbiAgICB9XG4gICAgdGhpcy5fcmVxdWVzdExvY2tJbnRlcnZhbCA9IHNldEludGVydmFsKCgpID0+IHtcbiAgICAgIGlmICh0aGlzLndzY29ubmVjdGVkKSB7XG4gICAgICAgIC8vIHRyeSB0byBhY3F1aXJlIGxvY2tcbiAgICAgICAgdGhpcy5fc2VuZE1lc3NhZ2UobmV3IFVpbnQ4QXJyYXkoWzEyN10pKTtcbiAgICAgIH1cbiAgICB9LCA1MDApO1xuICAgIGxldCByZXNvbHZlOiBhbnksIHJlamVjdDogYW55O1xuICAgIGNvbnN0IHByb21pc2U6IFByb21pc2U8bnVtYmVyPiA9IG5ldyBQcm9taXNlKChfcmVzb2x2ZSwgX3JlamVjdCkgPT4ge1xuICAgICAgcmVzb2x2ZSA9IF9yZXNvbHZlO1xuICAgICAgcmVqZWN0ID0gX3JlamVjdDtcbiAgICB9KTtcbiAgICB0aGlzLl9jdXJyZW50TG9ja1JlcXVlc3QgPSB7IHByb21pc2UsIHJlc29sdmUsIHJlamVjdCB9O1xuICAgIHJldHVybiBwcm9taXNlO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbGVhc2UgYSBsb2NrLlxuICAgKlxuICAgKiBAcGFyYW0gbG9jayBUaGUgbG9jayB0byByZWxlYXNlLlxuICAgKi9cbiAgcmVsZWFzZUxvY2sobG9jazogbnVtYmVyKTogdm9pZCB7XG4gICAgY29uc3QgZW5jb2RlciA9IGVuY29kaW5nLmNyZWF0ZUVuY29kZXIoKTtcbiAgICAvLyByZXBseSB3aXRoIHJlbGVhc2UgbG9ja1xuICAgIGVuY29kaW5nLndyaXRlVmFyVWludChlbmNvZGVyLCAxMjYpO1xuICAgIGVuY29kaW5nLndyaXRlVWludDMyKGVuY29kZXIsIGxvY2spO1xuICAgIC8vIHJlbGVhc2luZyBsb2NrXG4gICAgdGhpcy5fc2VuZE1lc3NhZ2UoZW5jb2RpbmcudG9VaW50OEFycmF5KGVuY29kZXIpKTtcbiAgICBpZiAodGhpcy5fcmVxdWVzdExvY2tJbnRlcnZhbCkge1xuICAgICAgY2xlYXJJbnRlcnZhbCh0aGlzLl9yZXF1ZXN0TG9ja0ludGVydmFsKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogU2VuZCBhIG5ldyBtZXNzYWdlIHRvIFdlYlNvY2tldCBzZXJ2ZXIuXG4gICAqXG4gICAqIEBwYXJhbSBtZXNzYWdlIFRoZSBtZXNzYWdlIHRvIHNlbmRcbiAgICovXG4gIHByaXZhdGUgX3NlbmRNZXNzYWdlKG1lc3NhZ2U6IFVpbnQ4QXJyYXkpOiB2b2lkIHtcbiAgICAvLyBzZW5kIG9uY2UgY29ubmVjdGVkXG4gICAgY29uc3Qgc2VuZCA9ICgpID0+IHtcbiAgICAgIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgICBpZiAodGhpcy53c2Nvbm5lY3RlZCkge1xuICAgICAgICAgIHRoaXMud3MhLnNlbmQobWVzc2FnZSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgdGhpcy5vbmNlKCdzdGF0dXMnLCBzZW5kKTtcbiAgICAgICAgfVxuICAgICAgfSwgMCk7XG4gICAgfTtcbiAgICBzZW5kKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIHRoZSBjb25uZWN0aW9uIHN0YXR1cy5cbiAgICpcbiAgICogQHBhcmFtIHN0YXR1cyBUaGUgY29ubmVjdGlvbiBzdGF0dXMuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9vbkNvbm5lY3Rpb25TdGF0dXMoc3RhdHVzOiB7XG4gICAgc3RhdHVzOiAnY29ubmVjdGVkJyB8ICdkaXNjb25uZWN0ZWQnO1xuICB9KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgaWYgKHRoaXMuX2lzSW5pdGlhbGl6ZWQgJiYgc3RhdHVzLnN0YXR1cyA9PT0gJ2Nvbm5lY3RlZCcpIHtcbiAgICAgIGNvbnN0IGxvY2sgPSBhd2FpdCB0aGlzLmFjcXVpcmVMb2NrKCk7XG4gICAgICBjb25zdCBjb250ZW50SXNJbml0aWFsaXplZCA9IGF3YWl0IHRoaXMucmVxdWVzdEluaXRpYWxDb250ZW50KCk7XG4gICAgICBpZiAoIWNvbnRlbnRJc0luaXRpYWxpemVkKSB7XG4gICAgICAgIHRoaXMucHV0SW5pdGlhbGl6ZWRTdGF0ZSgpO1xuICAgICAgfVxuICAgICAgdGhpcy5yZWxlYXNlTG9jayhsb2NrKTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9wYXRoOiBzdHJpbmc7XG4gIHByaXZhdGUgX2NvbnRlbnRUeXBlOiBzdHJpbmc7XG4gIHByaXZhdGUgX3NlcnZlclVybDogc3RyaW5nO1xuICBwcml2YXRlIF9pc0luaXRpYWxpemVkOiBib29sZWFuO1xuICBwcml2YXRlIF9yZXF1ZXN0TG9ja0ludGVydmFsOiBudW1iZXI7XG4gIHByaXZhdGUgX2N1cnJlbnRMb2NrUmVxdWVzdDoge1xuICAgIHByb21pc2U6IFByb21pc2U8bnVtYmVyPjtcbiAgICByZXNvbHZlOiAobG9jazogbnVtYmVyKSA9PiB2b2lkO1xuICAgIHJlamVjdDogKCkgPT4gdm9pZDtcbiAgfSB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9pbml0aWFsQ29udGVudFJlcXVlc3Q6IFByb21pc2VEZWxlZ2F0ZTxib29sZWFuPiB8IG51bGwgPSBudWxsO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBXZWJTb2NrZXRQcm92aWRlcldpdGhMb2NrcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFdlYlNvY2tldFByb3ZpZGVyV2l0aExvY2tzIHtcbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGEgV2ViU29ja2V0UHJvdmlkZXJXaXRoTG9ja3MuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIGV4dGVuZHMgSURvY3VtZW50UHJvdmlkZXJGYWN0b3J5LklPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgc2VydmVyIFVSTFxuICAgICAqL1xuICAgIHVybDogc3RyaW5nO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9