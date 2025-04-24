"use strict";
(self["webpackChunkipyaudio"] = self["webpackChunkipyaudio"] || []).push([["lib_player_js-lib_recorder_js-data_image_svg_xml_3csvg_xmlns_27http_www_w3_org_2000_svg_27_vi-4e62a2"],{

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./lib/chunk_queue.js":
/*!****************************!*\
  !*** ./lib/chunk_queue.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports) {


// Copyright (c) Zhendong Peng
// Distributed under the terms of the Modified BSD License.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
class ChunkQueue {
    constructor() {
        this.queue = [];
        this.resolveDequeue = null;
        this.waitingDequeue = null;
    }
    mergeAllChunks() {
        if (this.queue.length === 0) {
            return new Uint8Array(0);
        }
        let totalLength = 0;
        for (const chunk of this.queue) {
            totalLength += chunk.length;
        }
        const merged = new Uint8Array(totalLength);
        let offset = 0;
        for (const chunk of this.queue) {
            merged.set(chunk, offset);
            offset += chunk.length;
        }
        return merged;
    }
    enqueue(chunk) {
        this.queue.push(chunk);
        if (this.resolveDequeue) {
            const merged = this.mergeAllChunks();
            this.resolveDequeue(merged);
            this.queue.length = 0;
            this.resolveDequeue = null;
            this.waitingDequeue = null;
        }
    }
    dequeue(timeoutMs = 0) {
        return __awaiter(this, void 0, void 0, function* () {
            if (this.queue.length > 0) {
                const merged = this.mergeAllChunks();
                this.queue.length = 0;
                return merged;
            }
            if (!this.waitingDequeue) {
                this.waitingDequeue = new Promise((resolve) => {
                    this.resolveDequeue = resolve;
                });
                if (timeoutMs > 0) {
                    const timeout = setTimeout(() => {
                        if (this.resolveDequeue) {
                            this.resolveDequeue(new Uint8Array(0));
                            this.resolveDequeue = null;
                            this.waitingDequeue = null;
                        }
                    }, timeoutMs);
                    this.waitingDequeue
                        .then(() => {
                        if (timeout) {
                            clearTimeout(timeout);
                        }
                    })
                        .catch(() => {
                        if (timeout) {
                            clearTimeout(timeout);
                        }
                    });
                }
            }
            return this.waitingDequeue;
        });
    }
    get length() {
        return this.queue.length;
    }
}
exports["default"] = ChunkQueue;


/***/ }),

/***/ "./lib/player.js":
/*!***********************!*\
  !*** ./lib/player.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) Zhendong Peng
// Distributed under the terms of the Modified BSD License.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.PlayerView = exports.PlayerModel = void 0;
const merge_1 = __importDefault(__webpack_require__(/*! lodash/merge */ "./node_modules/lodash/merge.js"));
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base?ea51");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const player_1 = __importDefault(__webpack_require__(/*! ./wavesurfer/player */ "./lib/wavesurfer/player.js"));
// Import the CSS
__webpack_require__(/*! bootstrap/dist/css/bootstrap.min.css */ "./node_modules/bootstrap/dist/css/bootstrap.min.css");
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
class PlayerModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: PlayerModel.model_name, _model_module: PlayerModel.model_module, _model_module_version: PlayerModel.model_module_version, _view_name: PlayerModel.view_name, _view_module: PlayerModel.view_module, _view_module_version: PlayerModel.view_module_version });
    }
}
exports.PlayerModel = PlayerModel;
PlayerModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
PlayerModel.model_name = 'PlayerModel';
PlayerModel.model_module = version_1.MODULE_NAME;
PlayerModel.model_module_version = version_1.MODULE_VERSION;
PlayerModel.view_name = 'PlayerView'; // Set to null if no view
PlayerModel.view_module = version_1.MODULE_NAME; // Set to null if no view
PlayerModel.view_module_version = version_1.MODULE_VERSION;
class PlayerView extends base_1.DOMWidgetView {
    render() {
        super.render();
        this.displayed.then(() => __awaiter(this, void 0, void 0, function* () {
            const config = {
                isStreaming: this.model.get('is_streaming'),
                language: this.model.get('language'),
            };
            this._player = player_1.default.create((0, merge_1.default)({}, this.model.get('config'), config));
            this.el.appendChild(this._player.el);
            this.model.on('change:audio', () => {
                this._player.sampleRate = this.model.get('rate');
                this._player.load(this.model.get('audio'));
            });
            this.model.on('change:is_done', () => {
                this._player.setDone();
            });
        }));
    }
}
exports.PlayerView = PlayerView;


/***/ }),

/***/ "./lib/recorder.js":
/*!*************************!*\
  !*** ./lib/recorder.js ***!
  \*************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) Zhendong Peng
// Distributed under the terms of the Modified BSD License.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.RecorderView = exports.RecorderModel = void 0;
const merge_1 = __importDefault(__webpack_require__(/*! lodash/merge */ "./node_modules/lodash/merge.js"));
const jupyter_dataserializers_1 = __webpack_require__(/*! jupyter-dataserializers */ "webpack/sharing/consume/default/jupyter-dataserializers/jupyter-dataserializers");
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base?ea51");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const chunk_queue_1 = __importDefault(__webpack_require__(/*! ./chunk_queue */ "./lib/chunk_queue.js"));
const recorder_1 = __importDefault(__webpack_require__(/*! ./wavesurfer/recorder */ "./lib/wavesurfer/recorder.js"));
// Import the CSS
__webpack_require__(/*! bootstrap/dist/css/bootstrap.min.css */ "./node_modules/bootstrap/dist/css/bootstrap.min.css");
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
class RecorderModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: RecorderModel.model_name, _model_module: RecorderModel.model_module, _model_module_version: RecorderModel.model_module_version, _view_name: RecorderModel.view_name, _view_module: RecorderModel.view_module, _view_module_version: RecorderModel.view_module_version, chunk: new Uint8Array(0), rate: 16000, end: false });
    }
}
exports.RecorderModel = RecorderModel;
RecorderModel.serializers = Object.assign(Object.assign({}, base_1.DOMWidgetModel.serializers), { 
    // Add any extra serializers here
    chunk: jupyter_dataserializers_1.simplearray_serialization });
RecorderModel.model_name = 'RecorderModel';
RecorderModel.model_module = version_1.MODULE_NAME;
RecorderModel.model_module_version = version_1.MODULE_VERSION;
RecorderModel.view_name = 'RecorderView'; // Set to null if no view
RecorderModel.view_module = version_1.MODULE_NAME; // Set to null if no view
RecorderModel.view_module_version = version_1.MODULE_VERSION;
class RecorderView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this._chunks = new chunk_queue_1.default();
        this._isFirstChunk = true;
        this._isCompleted = false;
    }
    _sendChunk() {
        var _a;
        return __awaiter(this, void 0, void 0, function* () {
            // 1 seconds maximum wait time
            const chunk = yield this._chunks.dequeue(1000 + ((_a = this._recorder.timeSlice) !== null && _a !== void 0 ? _a : 20));
            if (chunk.length > 0) {
                this.model.set('chunk', { array: chunk, shape: [chunk.length] });
                this.model.save_changes();
            }
            if (this._isCompleted) {
                this.model.set('completed', true);
                this.model.save_changes();
            }
        });
    }
    render() {
        super.render();
        this.displayed.then(() => __awaiter(this, void 0, void 0, function* () {
            const language = this.model.get('language');
            this._recorder = recorder_1.default.create((0, merge_1.default)({}, this.model.get('config'), { language }), (0, merge_1.default)({}, this.model.get('player_config'), { language }));
            this.el.appendChild(this._recorder.el);
            this.model.on('msg:custom', (msg) => __awaiter(this, void 0, void 0, function* () {
                if (msg.msg_type === 'chunk_received') {
                    this._sendChunk();
                }
            }));
            this._recorder.onRecordStart(() => {
                this._isCompleted = false;
                this._isFirstChunk = true;
                this.model.set('completed', false);
                this.model.set('rate', this._recorder.sampleRate);
                this.model.save_changes();
            });
            this._recorder.onRecordChunk((blob) => __awaiter(this, void 0, void 0, function* () {
                this._chunks.enqueue(new Uint8Array(yield blob.arrayBuffer()));
                if (this.model.get('sync') && this._isFirstChunk) {
                    this._isFirstChunk = false;
                    this._sendChunk();
                }
            }));
            this._recorder.onRecordEnd((blob) => __awaiter(this, void 0, void 0, function* () {
                this._isCompleted = true;
                if (!this.model.get('sync')) {
                    this.model.set('completed', true);
                    this.model.save_changes();
                }
            }));
        }));
    }
}
exports.RecorderView = RecorderView;


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Zhendong Peng
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/wavesurfer/pcm_player.js":
/*!**************************************!*\
  !*** ./lib/wavesurfer/pcm_player.js ***!
  \**************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) Zhendong Peng
// Distributed under the terms of the Modified BSD License.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.PCMPlayer = void 0;
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/wavesurfer/utils.js");
class PCMPlayer {
    constructor(options) {
        this._isDone = false;
        this._isPlaying = true;
        this._samples = new Int16Array(0);
        this._allSamples = new Int16Array(0);
        this._options = Object.assign({ channels: 1, sampleRate: 16000, flushTime: 100, language: 'en' }, options);
        this.playButton = (0, utils_1.createElement)('button', 'btn btn-danger me-3 my-3', '<i class="fa fa-pause"></i>');
        this.playButton.onclick = () => {
            this._isPlaying = !this._isPlaying;
            this._isPlaying ? this.play() : this.pause();
            this.playButton.innerHTML = `<i class="fa fa-${this._isPlaying ? 'pause' : 'play'}"></i>`;
        };
        this._interval = window.setInterval(this.flush.bind(this), this._options.flushTime);
        this._audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        this._gainNode = this._audioCtx.createGain();
        this._gainNode.gain.value = 1.0;
        this._gainNode.connect(this._audioCtx.destination);
        this._startTime = this._audioCtx.currentTime;
    }
    set sampleRate(rate) {
        this._options.sampleRate = rate;
    }
    setDone() {
        this._isDone = true;
    }
    feed(base64Data) {
        const binaryString = atob(base64Data);
        const buffer = new ArrayBuffer(binaryString.length);
        const bufferView = new Uint8Array(buffer);
        for (let i = 0; i < binaryString.length; i++) {
            bufferView[i] = binaryString.charCodeAt(i);
        }
        const data = new Int16Array(buffer);
        this._samples = new Int16Array([...this._samples, ...data]);
        this._allSamples = new Int16Array([...this._allSamples, ...data]);
    }
    get url() {
        return (0, utils_1.createObjectURL)(this._allSamples.buffer, {
            numChannels: this._options.channels,
            sampleRate: this._options.sampleRate,
        });
    }
    flush() {
        if (!this._samples.length) {
            return;
        }
        const isDone = this._isDone;
        const bufferSource = this._audioCtx.createBufferSource();
        const length = this._samples.length / this._options.channels;
        const audioBuffer = this._audioCtx.createBuffer(this._options.channels, length, this._options.sampleRate);
        for (let channel = 0; channel < this._options.channels; channel++) {
            const audioData = audioBuffer.getChannelData(channel);
            let offset = channel;
            for (let i = 0; i < length; i++) {
                audioData[i] = this._samples[offset] / 32768;
                offset += this._options.channels;
            }
        }
        this._startTime = Math.max(this._startTime, this._audioCtx.currentTime);
        bufferSource.buffer = audioBuffer;
        bufferSource.connect(this._gainNode);
        bufferSource.start(this._startTime);
        bufferSource.onended = () => {
            this.playButton.disabled = isDone ? true : false;
        };
        this._startTime += audioBuffer.duration;
        this._samples = new Int16Array(0);
    }
    play() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this._audioCtx.resume();
        });
    }
    pause() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this._audioCtx.suspend();
        });
    }
    volume(volume) {
        this._gainNode.gain.value = volume;
    }
    destroy() {
        if (this._interval) {
            clearInterval(this._interval);
        }
        this._samples = new Int16Array(0);
        this._audioCtx.close();
    }
}
exports.PCMPlayer = PCMPlayer;
exports["default"] = PCMPlayer;


/***/ }),

/***/ "./lib/wavesurfer/player.js":
/*!**********************************!*\
  !*** ./lib/wavesurfer/player.js ***!
  \**********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) Zhendong Peng
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const wavesurfer_js_1 = __importDefault(__webpack_require__(/*! wavesurfer.js */ "./node_modules/wavesurfer.js/dist/wavesurfer.cjs"));
const hover_js_1 = __importDefault(__webpack_require__(/*! wavesurfer.js/dist/plugins/hover.js */ "./node_modules/wavesurfer.js/dist/plugins/hover.cjs"));
const minimap_js_1 = __importDefault(__webpack_require__(/*! wavesurfer.js/dist/plugins/minimap.js */ "./node_modules/wavesurfer.js/dist/plugins/minimap.cjs"));
const spectrogram_js_1 = __importDefault(__webpack_require__(/*! wavesurfer.js/dist/plugins/spectrogram.js */ "./node_modules/wavesurfer.js/dist/plugins/spectrogram.cjs"));
const timeline_js_1 = __importDefault(__webpack_require__(/*! wavesurfer.js/dist/plugins/timeline.js */ "./node_modules/wavesurfer.js/dist/plugins/timeline.cjs"));
const zoom_js_1 = __importDefault(__webpack_require__(/*! wavesurfer.js/dist/plugins/zoom.js */ "./node_modules/wavesurfer.js/dist/plugins/zoom.cjs"));
const pcm_player_1 = __importDefault(__webpack_require__(/*! ./pcm_player */ "./lib/wavesurfer/pcm_player.js"));
const reward_1 = __webpack_require__(/*! ./reward */ "./lib/wavesurfer/reward.js");
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/wavesurfer/utils.js");
class Player {
    constructor(config) {
        this.el = (0, utils_1.createElement)('div', 'lm-Widget');
        this._container = (0, utils_1.createElement)('div', 'waveform');
        this._duration = (0, utils_1.createElement)('div', 'duration', '0:00');
        this._currentTime = (0, utils_1.createElement)('div', 'time', '0:00');
        this._container.append(this._duration, this._currentTime);
        this.el.append(this._container);
        this._config = config;
    }
    get url() {
        if (this._config.isStreaming) {
            return this._pcmPlayer.url;
        }
        else {
            return (0, utils_1.createObjectURL)(this._wavesurfer.getDecodedData());
        }
    }
    set sampleRate(rate) {
        if (this._config.isStreaming) {
            this._pcmPlayer.sampleRate = rate;
        }
        this._wavesurfer.options.sampleRate = rate;
    }
    load(url) {
        if (this._config.isStreaming) {
            this._pcmPlayer.feed(url);
            this._wavesurfer.load(this.url);
        }
        else {
            this._wavesurfer.load(url);
        }
    }
    setDone() {
        this._pcmPlayer.setDone();
    }
    createPCMPlayer() {
        if (this._config.isStreaming) {
            this._pcmPlayer = new pcm_player_1.default({
                channels: 1,
                sampleRate: this._config.options.sampleRate,
            });
            this.el.append(this._pcmPlayer.playButton);
        }
    }
    createDownloadButton() {
        const downloadButton = (0, utils_1.createElement)('button', 'btn btn-success my-3');
        const label = this._config.language === 'zh' ? '下载' : 'Download';
        downloadButton.innerHTML = `${label} <i class="fa fa-download"></i>`;
        downloadButton.onclick = () => {
            const link = document.createElement('a');
            link.href = this.url;
            link.download = 'audio.wav';
            link.click();
        };
        this.el.append(downloadButton);
    }
    static createPlugins(config) {
        var _a;
        const pluginMap = {
            hover: () => { var _a; return hover_js_1.default.create((_a = config.pluginOptions) === null || _a === void 0 ? void 0 : _a.hover); },
            minimap: () => {
                var _a, _b;
                return minimap_js_1.default.create(Object.assign(Object.assign({}, (_a = config.pluginOptions) === null || _a === void 0 ? void 0 : _a.minimap), { plugins: [
                        hover_js_1.default.create(Object.assign(Object.assign({}, (_b = config.pluginOptions) === null || _b === void 0 ? void 0 : _b.hover), { lineWidth: 1 })),
                    ] }));
            },
            spectrogram: () => { var _a; return spectrogram_js_1.default.create((_a = config.pluginOptions) === null || _a === void 0 ? void 0 : _a.spectrogram); },
            timeline: () => { var _a; return timeline_js_1.default.create((_a = config.pluginOptions) === null || _a === void 0 ? void 0 : _a.timeline); },
            zoom: () => { var _a; return zoom_js_1.default.create((_a = config.pluginOptions) === null || _a === void 0 ? void 0 : _a.zoom); },
        };
        return Array.from((_a = config.plugins) !== null && _a !== void 0 ? _a : [])
            .map((plugin) => { var _a; return (_a = pluginMap[plugin]) === null || _a === void 0 ? void 0 : _a.call(pluginMap); })
            .filter(Boolean);
    }
    createWaveSurfer() {
        this._wavesurfer = wavesurfer_js_1.default.create(Object.assign(Object.assign({}, this._config.options), { container: this._container, plugins: Player.createPlugins(this._config) }));
        this._wavesurfer.on('interaction', () => this._wavesurfer.playPause());
        this._wavesurfer.on('decode', (time) => (this._duration.textContent = (0, utils_1.formatTime)(time)));
        this._wavesurfer.on('timeupdate', (time) => (this._currentTime.textContent = (0, utils_1.formatTime)(time)));
    }
    static create(config) {
        const instance = new Player(config);
        instance.createWaveSurfer();
        instance.createPCMPlayer();
        instance.createDownloadButton();
        instance.el.appendChild((0, reward_1.createRewardDropdown)(config.language || 'en'));
        return instance;
    }
}
exports["default"] = Player;


/***/ }),

/***/ "./lib/wavesurfer/recorder.js":
/*!************************************!*\
  !*** ./lib/wavesurfer/recorder.js ***!
  \************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) Zhendong Peng
// Distributed under the terms of the Modified BSD License.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const wavesurfer_js_1 = __importDefault(__webpack_require__(/*! wavesurfer.js */ "./node_modules/wavesurfer.js/dist/wavesurfer.cjs"));
const record_js_1 = __importDefault(__webpack_require__(/*! wavesurfer.js/dist/plugins/record.js */ "./node_modules/wavesurfer.js/dist/plugins/record.cjs"));
const player_1 = __importDefault(__webpack_require__(/*! ./player */ "./lib/wavesurfer/player.js"));
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/wavesurfer/utils.js");
class Recorder {
    constructor(config, playerConfig) {
        this.el = (0, utils_1.createElement)('div', 'lm-Widget');
        this._container = (0, utils_1.createElement)('div', 'waveform');
        this._currentTime = (0, utils_1.createElement)('div', 'time', '0:00');
        this._container.append(this._currentTime);
        this._config = config;
        this._player = player_1.default.create(playerConfig);
    }
    get sampleRate() {
        return this._wavesurfer.options.sampleRate;
    }
    get timeSlice() {
        var _a;
        return (_a = this._config.recordOptions) === null || _a === void 0 ? void 0 : _a.mediaRecorderTimeslice;
    }
    set sampleRate(rate) {
        this._wavesurfer.options.sampleRate = rate;
        this._player.sampleRate = rate;
    }
    createWaveSurfer() {
        this._wavesurfer = wavesurfer_js_1.default.create(Object.assign(Object.assign({}, this._config.options), { container: this._container }));
    }
    createRateSelect() {
        this._rateSelect = (0, utils_1.createElement)('select', 'form-select-sm d-inline-block me-3 my-3 w-25');
        const rates = [8000, 16000, 22050, 24000, 44100, 48000];
        rates.forEach((rate) => {
            const option = document.createElement('option');
            option.value = rate.toString();
            option.text = `${rate} Hz`;
            if (rate === 16000) {
                option.selected = true;
            }
            this._rateSelect.appendChild(option);
        });
    }
    createMicSelect() {
        this._micSelect = (0, utils_1.createElement)('select', 'form-select-sm d-inline-block me-3 my-3 w-50');
        navigator.mediaDevices
            .getUserMedia({ audio: true, video: false })
            .then((stream) => {
            record_js_1.default.getAvailableAudioDevices().then((devices) => {
                devices.forEach((device) => {
                    const option = document.createElement('option');
                    option.value = device.deviceId;
                    option.text = device.label || device.deviceId;
                    this._micSelect.appendChild(option);
                });
            });
        })
            .catch((err) => {
            const label = this._config.language === 'zh' ? '访问麦克风失败' : 'Error accessing the microphone: ';
            throw new Error(label + err.message);
        });
    }
    createPauseButton() {
        this._pauseButton = (0, utils_1.createElement)('button', 'btn btn-outline-danger me-3 my-3', '<i class="fa fa-pause"></i>');
        this._pauseButton.disabled = true;
        this._pauseButton.onclick = () => {
            if (this._recorder.isRecording()) {
                this._recorder.pauseRecording();
                this._pauseButton.innerHTML = '<i class="fa fa-play"></i>';
                this._container.style.display = 'none';
                this._player.el.style.display = 'block';
            }
            else {
                this._recorder.resumeRecording();
                this._pauseButton.innerHTML = '<i class="fa fa-pause"></i>';
                this._container.style.display = 'block';
                this._player.el.style.display = 'none';
            }
        };
    }
    createRecordButton() {
        this._recordButton = (0, utils_1.createElement)('button', 'btn btn-danger me-3 my-3', '<i class="fa fa-microphone"></i>');
        this._recordButton.onclick = () => {
            if (this._recorder.isRecording() || this._recorder.isPaused()) {
                this._recorder.stopRecording();
                this._container.style.display = 'none';
                this._player.el.style.display = 'block';
            }
            else {
                this._wavesurfer.options.normalize = false;
                this.sampleRate = parseInt(this._rateSelect.value);
                this._recorder.startRecording({ deviceId: this._micSelect.value }).then(() => {
                    this._pauseButton.disabled = false;
                    this._rateSelect.disabled = true;
                    this._micSelect.disabled = true;
                    this._pauseButton.innerHTML = '<i class="fa fa-pause"></i>';
                    this._recordButton.innerHTML = '<i class="fa fa-stop"></i>';
                    this._container.style.display = 'block';
                    this._player.el.style.display = 'none';
                });
            }
        };
    }
    onRecordStart(callback) {
        this._recorder.on('record-start', () => {
            callback();
        });
    }
    onRecordChunk(callback) {
        this._recorder.on('record-data-available', (blob) => {
            callback(blob);
        });
    }
    onRecordEnd(callback) {
        this._recorder.on('record-end', (blob) => __awaiter(this, void 0, void 0, function* () {
            this._player.load(URL.createObjectURL(blob));
            this._recordButton.disabled = true;
            this._pauseButton.disabled = true;
            yield callback(blob);
            this._recordButton.disabled = false;
            this._pauseButton.disabled = true;
            this._rateSelect.disabled = false;
            this._micSelect.disabled = false;
            this._pauseButton.innerHTML = '<i class="fa fa-play"></i>';
            this._recordButton.innerHTML = '<i class="fa fa-microphone"></i>';
        }));
    }
    createRecorder() {
        this._wavesurfer.toggleInteraction(false);
        this._recorder = this._wavesurfer.registerPlugin(record_js_1.default.create(this._config.recordOptions));
        this.createRateSelect();
        this.createMicSelect();
        this.createPauseButton();
        this.createRecordButton();
        this._container.style.display = 'none';
        this._player.el.style.display = 'none';
        this.el.append(this._recordButton, this._pauseButton, this._rateSelect, this._micSelect, this._container, this._player.el);
        this._recorder.on('record-pause', (blob) => {
            this._player.load(URL.createObjectURL(blob));
        });
        this._recorder.on('record-progress', (time) => {
            this._currentTime.textContent = (0, utils_1.formatTime)(time / 1000);
        });
    }
    static create(config, playerConfig) {
        const instance = new Recorder(config, playerConfig);
        instance.createWaveSurfer();
        instance.createRecorder();
        return instance;
    }
}
exports["default"] = Recorder;


/***/ }),

/***/ "./lib/wavesurfer/reward.js":
/*!**********************************!*\
  !*** ./lib/wavesurfer/reward.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Zhendong Peng
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.createRewardDropdown = void 0;
__webpack_require__(/*! bootstrap/dist/js/bootstrap.bundle.min.js */ "./node_modules/bootstrap/dist/js/bootstrap.bundle.min.js");
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/wavesurfer/utils.js");
function createRewardDropdown(language) {
    const rewardDropdown = (0, utils_1.createElement)('div', 'dropdown my-3 float-end text-end');
    const dropdownButton = (0, utils_1.createElement)('button', 'btn btn-warning dropdown-toggle');
    dropdownButton.setAttribute('data-bs-toggle', 'dropdown');
    dropdownButton.innerHTML =
        language === 'zh' ? '<i class="fa fa-thumbs-o-up"></i> 赞赏' : '<i class="fa fa-coffee"></i> Buy me a coffee';
    const dropdownMenu = (0, utils_1.createElement)('ul', 'dropdown-menu p-2');
    const url = 'https://modelscope.cn/models/pengzhendong/pengzhendong/resolve/master/images';
    const rewards = [
        {
            imgSrc: `${url}/wechat-reward.jpg`,
            name: language === 'zh' ? '微信' : 'WeChat',
        },
        {
            imgSrc: `${url}/alipay-reward.jpg`,
            name: language === 'zh' ? '支付宝' : 'AliPay',
        },
    ];
    const table = (0, utils_1.createElement)('table', 'table table-bordered mb-0');
    const tbody = (0, utils_1.createElement)('tbody');
    const imageRow = (0, utils_1.createElement)('tr');
    rewards.forEach((reward) => {
        const cell = (0, utils_1.createElement)('td', 'text-center p-2');
        cell.style.width = `${100 / rewards.length}%`;
        const img = (0, utils_1.createElement)('img', 'img-fluid d-block mx-auto');
        img.src = reward.imgSrc;
        cell.appendChild(img);
        const name = (0, utils_1.createElement)('div', 'text-center mt-2 fw-bold');
        name.textContent = reward.name;
        cell.appendChild(name);
        imageRow.appendChild(cell);
    });
    tbody.appendChild(imageRow);
    table.appendChild(tbody);
    const dropdownItem = (0, utils_1.createElement)('li', '');
    dropdownItem.appendChild(table);
    dropdownMenu.appendChild(dropdownItem);
    const link = (0, utils_1.createElement)('a');
    link.href = 'https://github.com/pengzhendong/ipyaudio';
    link.target = '_blank';
    const starBadge = (0, utils_1.createElement)('img', 'img-fluid me-3');
    starBadge.src = 'https://img.shields.io/github/stars/pengzhendong/ipyaudio.svg';
    link.appendChild(starBadge);
    rewardDropdown.appendChild(link);
    rewardDropdown.appendChild(dropdownButton);
    rewardDropdown.appendChild(dropdownMenu);
    return rewardDropdown;
}
exports.createRewardDropdown = createRewardDropdown;


/***/ }),

/***/ "./lib/wavesurfer/utils.js":
/*!*********************************!*\
  !*** ./lib/wavesurfer/utils.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, exports) => {


// Copyright (c) Zhendong Peng
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.createObjectURL = exports.formatTime = exports.createElement = void 0;
const createElement = (tagName, className = '', innerHTML = '') => {
    const element = document.createElement(tagName);
    element.className = className;
    element.innerHTML = innerHTML;
    return element;
};
exports.createElement = createElement;
const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const secondsRemainder = Math.round(seconds) % 60;
    const paddedSeconds = `0${secondsRemainder}`.slice(-2);
    return `${minutes}:${paddedSeconds}`;
};
exports.formatTime = formatTime;
function getWavHeader(options) {
    const numFrames = options.numFrames;
    const numChannels = options.numChannels || 2;
    const sampleRate = options.sampleRate || 44100;
    const bytesPerSample = options.isFloat ? 4 : 2;
    const format = options.isFloat ? 3 : 1;
    const blockAlign = numChannels * bytesPerSample;
    const byteRate = sampleRate * blockAlign;
    const dataSize = numFrames * blockAlign;
    const buffer = new ArrayBuffer(44);
    const dv = new DataView(buffer);
    let p = 0;
    function writeString(s) {
        for (let i = 0; i < s.length; i++) {
            dv.setUint8(p + i, s.charCodeAt(i));
        }
        p += s.length;
    }
    function writeUint32(d) {
        dv.setUint32(p, d, true);
        p += 4;
    }
    function writeUint16(d) {
        dv.setUint16(p, d, true);
        p += 2;
    }
    writeString('RIFF'); // ChunkID
    writeUint32(dataSize + 36); // ChunkSize
    writeString('WAVE'); // Format
    writeString('fmt '); // Subchunk1ID
    writeUint32(16); // Subchunk1Size
    writeUint16(format); // AudioFormat https://i.stack.imgur.com/BuSmb.png
    writeUint16(numChannels); // NumChannels
    writeUint32(sampleRate); // SampleRate
    writeUint32(byteRate); // ByteRate
    writeUint16(blockAlign); // BlockAlign
    writeUint16(bytesPerSample * 8); // BitsPerSample
    writeString('data'); // Subchunk2ID
    writeUint32(dataSize); // Subchunk2Size
    return new Uint8Array(buffer);
}
function interleaveChannels(buffer) {
    const { numberOfChannels, length } = buffer;
    const pcmData = new Int16Array(length * numberOfChannels);
    for (let channel = 0; channel < numberOfChannels; channel++) {
        const data = buffer.getChannelData(channel);
        const isFloat = data instanceof Float32Array;
        for (let i = 0; i < length; i++) {
            // convert float32 to int16
            pcmData[i * numberOfChannels + channel] = isFloat ? data[i] * 32767 : data[i];
        }
    }
    return pcmData;
}
function getWavBytes(buffer, options) {
    if (!buffer) {
        return new Uint8Array();
    }
    let headerBytes;
    let pcmData;
    if (buffer instanceof ArrayBuffer) {
        headerBytes = getWavHeader({
            isFloat: false,
            numChannels: options.numChannels,
            sampleRate: options.sampleRate,
            numFrames: buffer.byteLength / Int16Array.BYTES_PER_ELEMENT,
        });
        pcmData = new Uint8Array(buffer);
    }
    else {
        headerBytes = getWavHeader({
            isFloat: false,
            numChannels: buffer.numberOfChannels,
            sampleRate: buffer.sampleRate,
            numFrames: buffer.length,
        });
        pcmData = new Uint8Array(interleaveChannels(buffer).buffer);
    }
    const wavBytes = new Uint8Array(headerBytes.length + pcmData.length);
    wavBytes.set(headerBytes, 0);
    wavBytes.set(pcmData, headerBytes.length);
    return wavBytes;
}
const createObjectURL = (buffer, options = {
    numChannels: 1,
    sampleRate: 44100,
}) => {
    let wavBytes;
    if (buffer instanceof AudioBuffer) {
        wavBytes = getWavBytes(buffer, {
            numChannels: buffer.numberOfChannels,
            sampleRate: buffer.sampleRate,
        });
    }
    else {
        wavBytes = getWavBytes(buffer, options);
    }
    return URL.createObjectURL(new Blob([wavBytes], { type: 'audio/wav' }));
};
exports.createObjectURL = createObjectURL;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.waveform {
  background-color: black;
  cursor: pointer;
  position: relative;
  width: 100%;
}

.duration, .time {
  background: rgba(0, 0, 0, 0.75);
  color: #DDDD;
  font-size: 11px;
  position: absolute;
  bottom: 0;
  z-index: 11;
}

.duration { right: 0 }

.time { left: 0 }

.dropdown-menu {
  width: 500px;
  position: relative !important;
  transform: translateY(10px) !important;
}
`, "",{"version":3,"sources":["webpack://./css/widget.css"],"names":[],"mappings":"AAAA;EACE,uBAAuB;EACvB,eAAe;EACf,kBAAkB;EAClB,WAAW;AACb;;AAEA;EACE,+BAA+B;EAC/B,YAAY;EACZ,eAAe;EACf,kBAAkB;EAClB,SAAS;EACT,WAAW;AACb;;AAEA,YAAY,SAAS;;AAErB,QAAQ,QAAQ;;AAEhB;EACE,YAAY;EACZ,6BAA6B;EAC7B,sCAAsC;AACxC","sourcesContent":[".waveform {\n  background-color: black;\n  cursor: pointer;\n  position: relative;\n  width: 100%;\n}\n\n.duration, .time {\n  background: rgba(0, 0, 0, 0.75);\n  color: #DDDD;\n  font-size: 11px;\n  position: absolute;\n  bottom: 0;\n  z-index: 11;\n}\n\n.duration { right: 0 }\n\n.time { left: 0 }\n\n.dropdown-menu {\n  width: 500px;\n  position: relative !important;\n  transform: translateY(10px) !important;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = /*#__PURE__*/JSON.parse('{"name":"ipyaudio","version":"0.1.19","description":"A Custom Jupyter Widget Library","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/pengzhendong/ipyaudio","bugs":{"url":"https://github.com/pengzhendong/ipyaudio/issues"},"license":"BSD-3-Clause","author":{"name":"Zhendong Peng","email":"pzd17@tsinghua.org.cn"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"git+https://github.com/pengzhendong/ipyaudio.git"},"scripts":{"build":"jlpm run build:lib && jlpm run build:nbextension && jlpm run build:labextension:dev","build:prod":"jlpm run build:lib && jlpm run build:nbextension && jlpm run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"jlpm run clean:lib && jlpm run clean:nbextension && jlpm run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipyaudio/labextension","clean:nbextension":"rimraf ipyaudio/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"jlpm run build:lib","test":"jest","watch":"npm-run-all -p \\"watch:*\\"","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","bootstrap":"^5.3.5","jupyter-dataserializers":"^3.0.1","lodash.merge":"^4.6.2"},"devDependencies":{"@babel/core":"^7.23.7","@babel/preset-env":"^7.23.8","@jupyter-widgets/base-manager":"^1.0.7","@jupyterlab/builder":"^4.0.11","@lumino/application":"^2.3.0","@lumino/widgets":"^2.3.1","@types/jest":"^29.5.11","@types/webpack-env":"^1.18.4","@typescript-eslint/eslint-plugin":"^6.19.1","@typescript-eslint/parser":"^6.19.1","acorn":"^8.11.3","css-loader":"^6.9.1","eslint":"^8.56.0","eslint-config-prettier":"^9.1.0","eslint-plugin-prettier":"^5.1.3","fs-extra":"^11.2.0","identity-obj-proxy":"^3.0.0","jest":"^29.7.0","mkdirp":"^3.0.1","npm-run-all":"^4.1.5","prettier":"^3.2.4","rimraf":"^5.0.5","source-map-loader":"^5.0.0","style-loader":"^3.3.4","ts-jest":"^29.1.2","ts-loader":"^9.5.1","typescript":"~5.3.3","wavesurfer.js":"^7.9.1","webpack":"^5.90.0","webpack-cli":"^5.1.4"},"devDependenciesComments":{"@jupyterlab/builder":"pinned to the latest JupyterLab 3.x release","@lumino/application":"pinned to the latest Lumino 1.x release","@lumino/widgets":"pinned to the latest Lumino 1.x release"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipyaudio/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%272%27 fill=%27%23fff%27/%3e%3c/svg%3e":
/*!******************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%272%27 fill=%27%23fff%27/%3e%3c/svg%3e ***!
  \******************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%272%27 fill=%27%23fff%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%2386b7fe%27/%3e%3c/svg%3e":
/*!*********************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%2386b7fe%27/%3e%3c/svg%3e ***!
  \*********************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%2386b7fe%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%23fff%27/%3e%3c/svg%3e":
/*!******************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%23fff%27/%3e%3c/svg%3e ***!
  \******************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27%23fff%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%280, 0, 0, 0.25%29%27/%3e%3c/svg%3e":
/*!***********************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%280, 0, 0, 0.25%29%27/%3e%3c/svg%3e ***!
  \***********************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%280, 0, 0, 0.25%29%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%28255, 255, 255, 0.25%29%27/%3e%3c/svg%3e":
/*!*****************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%28255, 255, 255, 0.25%29%27/%3e%3c/svg%3e ***!
  \*****************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%27-4 -4 8 8%27%3e%3ccircle r=%273%27 fill=%27rgba%28255, 255, 255, 0.25%29%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 12 12%27 width=%2712%27 height=%2712%27 fill=%27none%27 stroke=%27%23dc3545%27%3e%3ccircle cx=%276%27 cy=%276%27 r=%274.5%27/%3e%3cpath stroke-linejoin=%27round%27 d=%27M5.8 3.6h.4L6 6.5z%27/%3e%3ccircle cx=%276%27 cy=%278.2%27 r=%27.6%27 fill=%27%23dc3545%27 stroke=%27none%27/%3e%3c/svg%3e":
/*!*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 12 12%27 width=%2712%27 height=%2712%27 fill=%27none%27 stroke=%27%23dc3545%27%3e%3ccircle cx=%276%27 cy=%276%27 r=%274.5%27/%3e%3cpath stroke-linejoin=%27round%27 d=%27M5.8 3.6h.4L6 6.5z%27/%3e%3ccircle cx=%276%27 cy=%278.2%27 r=%27.6%27 fill=%27%23dc3545%27 stroke=%27none%27/%3e%3c/svg%3e ***!
  \*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 12 12%27 width=%2712%27 height=%2712%27 fill=%27none%27 stroke=%27%23dc3545%27%3e%3ccircle cx=%276%27 cy=%276%27 r=%274.5%27/%3e%3cpath stroke-linejoin=%27round%27 d=%27M5.8 3.6h.4L6 6.5z%27/%3e%3ccircle cx=%276%27 cy=%278.2%27 r=%27.6%27 fill=%27%23dc3545%27 stroke=%27none%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23000%27%3e%3cpath d=%27M.293.293a1 1 0 0 1 1.414 0L8 6.586 14.293.293a1 1 0 1 1 1.414 1.414L9.414 8l6.293 6.293a1 1 0 0 1-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 0 1-1.414-1.414L6.586 8 .293 1.707a1 1 0 0 1 0-1.414%27/%3e%3c/svg%3e":
/*!*************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23000%27%3e%3cpath d=%27M.293.293a1 1 0 0 1 1.414 0L8 6.586 14.293.293a1 1 0 1 1 1.414 1.414L9.414 8l6.293 6.293a1 1 0 0 1-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 0 1-1.414-1.414L6.586 8 .293 1.707a1 1 0 0 1 0-1.414%27/%3e%3c/svg%3e ***!
  \*************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23000%27%3e%3cpath d=%27M.293.293a1 1 0 0 1 1.414 0L8 6.586 14.293.293a1 1 0 1 1 1.414 1.414L9.414 8l6.293 6.293a1 1 0 0 1-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 0 1-1.414-1.414L6.586 8 .293 1.707a1 1 0 0 1 0-1.414%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%236ea8fe%27%3e%3cpath fill-rule=%27evenodd%27 d=%27M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708%27/%3e%3c/svg%3e":
/*!***************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%236ea8fe%27%3e%3cpath fill-rule=%27evenodd%27 d=%27M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708%27/%3e%3c/svg%3e ***!
  \***************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%236ea8fe%27%3e%3cpath fill-rule=%27evenodd%27 d=%27M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0%27/%3e%3c/svg%3e":
/*!***********************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0%27/%3e%3c/svg%3e ***!
  \***********************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708%27/%3e%3c/svg%3e":
/*!************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708%27/%3e%3c/svg%3e ***!
  \************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27%23fff%27%3e%3cpath d=%27M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23052c65%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e":
/*!*******************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23052c65%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e ***!
  \*******************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23052c65%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23212529%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e":
/*!*******************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23212529%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e ***!
  \*******************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27 fill=%27none%27 stroke=%27%23212529%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpath d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23343a40%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e":
/*!****************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23343a40%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e ***!
  \****************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23343a40%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23dee2e6%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e":
/*!****************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23dee2e6%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e ***!
  \****************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3e%3cpath fill=%27none%27 stroke=%27%23dee2e6%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%272%27 d=%27m2 5 6 6 6-6%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27M6 10h8%27/%3e%3c/svg%3e":
/*!********************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27M6 10h8%27/%3e%3c/svg%3e ***!
  \********************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27M6 10h8%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27m6 10 3 3 6-6%27/%3e%3c/svg%3e":
/*!**************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27m6 10 3 3 6-6%27/%3e%3c/svg%3e ***!
  \**************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 20 20%27%3e%3cpath fill=%27none%27 stroke=%27%23fff%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27 stroke-width=%273%27 d=%27m6 10 3 3 6-6%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%28255, 255, 255, 0.55%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e":
/*!******************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%28255, 255, 255, 0.55%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e ***!
  \******************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%28255, 255, 255, 0.55%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%2833, 37, 41, 0.75%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e":
/*!***************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%2833, 37, 41, 0.75%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e ***!
  \***************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3e%3cpath stroke=%27rgba%2833, 37, 41, 0.75%29%27 stroke-linecap=%27round%27 stroke-miterlimit=%2710%27 stroke-width=%272%27 d=%27M4 7h22M4 15h22M4 23h22%27/%3e%3c/svg%3e";

/***/ }),

/***/ "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 8 8%27%3e%3cpath fill=%27%23198754%27 d=%27M2.3 6.73.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1%27/%3e%3c/svg%3e":
/*!*********************************************************************************************************************************************************************************************************************************************************!*\
  !*** data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 8 8%27%3e%3cpath fill=%27%23198754%27 d=%27M2.3 6.73.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1%27/%3e%3c/svg%3e ***!
  \*********************************************************************************************************************************************************************************************************************************************************/
/***/ ((module) => {

module.exports = "data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 8 8%27%3e%3cpath fill=%27%23198754%27 d=%27M2.3 6.73.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1%27/%3e%3c/svg%3e";

/***/ })

}]);
//# sourceMappingURL=lib_player_js-lib_recorder_js-data_image_svg_xml_3csvg_xmlns_27http_www_w3_org_2000_svg_27_vi-4e62a2.5626ffcb48021915d5fc.js.map