(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_imageviewer-extension_lib_index_js-_8dca1"],{

/***/ "../packages/imageviewer-extension/lib/index.js":
/*!******************************************************!*\
  !*** ../packages/imageviewer-extension/lib/index.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "addCommands": () => (/* binding */ addCommands)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/imageviewer */ "webpack/sharing/consume/default/@jupyterlab/imageviewer/@jupyterlab/imageviewer");
/* harmony import */ var _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module imageviewer-extension
 */




/**
 * The command IDs used by the image widget plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.resetImage = 'imageviewer:reset-image';
    CommandIDs.zoomIn = 'imageviewer:zoom-in';
    CommandIDs.zoomOut = 'imageviewer:zoom-out';
    CommandIDs.flipHorizontal = 'imageviewer:flip-horizontal';
    CommandIDs.flipVertical = 'imageviewer:flip-vertical';
    CommandIDs.rotateClockwise = 'imageviewer:rotate-clockwise';
    CommandIDs.rotateCounterclockwise = 'imageviewer:rotate-counterclockwise';
    CommandIDs.invertColors = 'imageviewer:invert-colors';
})(CommandIDs || (CommandIDs = {}));
/**
 * The list of file types for images.
 */
const FILE_TYPES = ['png', 'gif', 'jpeg', 'bmp', 'ico', 'tiff'];
/**
 * The name of the factory that creates image widgets.
 */
const FACTORY = 'Image';
/**
 * The name of the factory that creates image widgets.
 */
const TEXT_FACTORY = 'Image (Text)';
/**
 * The list of file types for images with optional text modes.
 */
const TEXT_FILE_TYPES = ['svg', 'xbm'];
/**
 * The test pattern for text file types in paths.
 */
const TEXT_FILE_REGEX = new RegExp(`[.](${TEXT_FILE_TYPES.join('|')})$`);
/**
 * The image file handler extension.
 */
const plugin = {
    activate,
    id: '@jupyterlab/imageviewer-extension:plugin',
    provides: _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2__.IImageTracker,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the image widget extension.
 */
function activate(app, translator, palette, restorer) {
    const trans = translator.load('jupyterlab');
    const namespace = 'image-widget';
    function onWidgetCreated(sender, widget) {
        var _a, _b;
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        void tracker.add(widget);
        const types = app.docRegistry.getFileTypesForPath(widget.context.path);
        if (types.length > 0) {
            widget.title.icon = types[0].icon;
            widget.title.iconClass = (_a = types[0].iconClass) !== null && _a !== void 0 ? _a : '';
            widget.title.iconLabel = (_b = types[0].iconLabel) !== null && _b !== void 0 ? _b : '';
        }
    }
    const factory = new _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2__.ImageViewerFactory({
        name: FACTORY,
        modelName: 'base64',
        fileTypes: [...FILE_TYPES, ...TEXT_FILE_TYPES],
        defaultFor: FILE_TYPES,
        readOnly: true
    });
    const textFactory = new _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2__.ImageViewerFactory({
        name: TEXT_FACTORY,
        modelName: 'text',
        fileTypes: TEXT_FILE_TYPES,
        defaultFor: TEXT_FILE_TYPES,
        readOnly: true
    });
    [factory, textFactory].forEach(factory => {
        app.docRegistry.addWidgetFactory(factory);
        factory.widgetCreated.connect(onWidgetCreated);
    });
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    if (restorer) {
        // Handle state restoration.
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({
                path: widget.context.path,
                factory: TEXT_FILE_REGEX.test(widget.context.path)
                    ? TEXT_FACTORY
                    : FACTORY
            }),
            name: widget => widget.context.path
        });
    }
    addCommands(app, tracker, translator);
    if (palette) {
        const category = trans.__('Image Viewer');
        [
            CommandIDs.zoomIn,
            CommandIDs.zoomOut,
            CommandIDs.resetImage,
            CommandIDs.rotateClockwise,
            CommandIDs.rotateCounterclockwise,
            CommandIDs.flipHorizontal,
            CommandIDs.flipVertical,
            CommandIDs.invertColors
        ].forEach(command => {
            palette.addItem({ command, category });
        });
    }
    return tracker;
}
/**
 * Add the commands for the image widget.
 */
function addCommands(app, tracker, translator) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    /**
     * Whether there is an active image viewer.
     */
    function isEnabled() {
        return (tracker.currentWidget !== null &&
            tracker.currentWidget === shell.currentWidget);
    }
    commands.addCommand('imageviewer:zoom-in', {
        execute: zoomIn,
        label: trans.__('Zoom In'),
        isEnabled
    });
    commands.addCommand('imageviewer:zoom-out', {
        execute: zoomOut,
        label: trans.__('Zoom Out'),
        isEnabled
    });
    commands.addCommand('imageviewer:reset-image', {
        execute: resetImage,
        label: trans.__('Reset Image'),
        isEnabled
    });
    commands.addCommand('imageviewer:rotate-clockwise', {
        execute: rotateClockwise,
        label: trans.__('Rotate Clockwise'),
        isEnabled
    });
    commands.addCommand('imageviewer:rotate-counterclockwise', {
        execute: rotateCounterclockwise,
        label: trans.__('Rotate Counterclockwise'),
        isEnabled
    });
    commands.addCommand('imageviewer:flip-horizontal', {
        execute: flipHorizontal,
        label: trans.__('Flip image horizontally'),
        isEnabled
    });
    commands.addCommand('imageviewer:flip-vertical', {
        execute: flipVertical,
        label: trans.__('Flip image vertically'),
        isEnabled
    });
    commands.addCommand('imageviewer:invert-colors', {
        execute: invertColors,
        label: trans.__('Invert Colors'),
        isEnabled
    });
    function zoomIn() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.scale = widget.scale > 1 ? widget.scale + 0.5 : widget.scale * 2;
        }
    }
    function zoomOut() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.scale = widget.scale > 1 ? widget.scale - 0.5 : widget.scale / 2;
        }
    }
    function resetImage() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.scale = 1;
            widget.colorinversion = 0;
            widget.resetRotationFlip();
        }
    }
    function rotateClockwise() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.rotateClockwise();
        }
    }
    function rotateCounterclockwise() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.rotateCounterclockwise();
        }
    }
    function flipHorizontal() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.flipHorizontal();
        }
    }
    function flipVertical() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.flipVertical();
        }
    }
    function invertColors() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.colorinversion += 1;
            widget.colorinversion %= 2;
        }
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaW1hZ2V2aWV3ZXItZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNOEI7QUFDcUM7QUFNckM7QUFDcUI7QUFFdEQ7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FnQm5CO0FBaEJELFdBQVUsVUFBVTtJQUNMLHFCQUFVLEdBQUcseUJBQXlCLENBQUM7SUFFdkMsaUJBQU0sR0FBRyxxQkFBcUIsQ0FBQztJQUUvQixrQkFBTyxHQUFHLHNCQUFzQixDQUFDO0lBRWpDLHlCQUFjLEdBQUcsNkJBQTZCLENBQUM7SUFFL0MsdUJBQVksR0FBRywyQkFBMkIsQ0FBQztJQUUzQywwQkFBZSxHQUFHLDhCQUE4QixDQUFDO0lBRWpELGlDQUFzQixHQUFHLHFDQUFxQyxDQUFDO0lBRS9ELHVCQUFZLEdBQUcsMkJBQTJCLENBQUM7QUFDMUQsQ0FBQyxFQWhCUyxVQUFVLEtBQVYsVUFBVSxRQWdCbkI7QUFFRDs7R0FFRztBQUNILE1BQU0sVUFBVSxHQUFHLENBQUMsS0FBSyxFQUFFLEtBQUssRUFBRSxNQUFNLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxNQUFNLENBQUMsQ0FBQztBQUVoRTs7R0FFRztBQUNILE1BQU0sT0FBTyxHQUFHLE9BQU8sQ0FBQztBQUV4Qjs7R0FFRztBQUNILE1BQU0sWUFBWSxHQUFHLGNBQWMsQ0FBQztBQUVwQzs7R0FFRztBQUNILE1BQU0sZUFBZSxHQUFHLENBQUMsS0FBSyxFQUFFLEtBQUssQ0FBQyxDQUFDO0FBRXZDOztHQUVHO0FBQ0gsTUFBTSxlQUFlLEdBQUcsSUFBSSxNQUFNLENBQUMsT0FBTyxlQUFlLENBQUMsSUFBSSxDQUFDLEdBQUcsQ0FBQyxJQUFJLENBQUMsQ0FBQztBQUV6RTs7R0FFRztBQUNI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UUFFOUMsSUFBSSxNQUFNLEVBQUU7WUFDVixNQUFNLENBQUMsZUFBZSxFQUFFLENBQUM7U0FDMUI7SUFDSCxDQUFDO0lBRUQsU0FBUyxzQkFBc0I7O1FBQzdCLE1BQU0sTUFBTSxTQUFHLE9BQU8sQ0FBQyxhQUFhLDBDQUFFLE9BQU8sQ0FBQztRQUU5QyxJQUFJLE1BQU0sRUFBRTtZQUNWLE1BQU0sQ0FBQyxzQkFBc0IsRUFBRSxDQUFDO1NBQ2pDO0lBQ0gsQ0FBQztJQUVELFNBQVMsY0FBYzs7UUFDckIsTUFBTSxNQUFNLFNBQUcsT0FBTyxDQUFDLGFBQWEsMENBQUUsT0FBTyxDQUFDO1FBRTlDLElBQUksTUFBTSxFQUFFO1lBQ1YsTUFBTSxDQUFDLGNBQWMsRUFBRSxDQUFDO1NBQ3pCO0lBQ0gsQ0FBQztJQUVELFNBQVMsWUFBWTs7UUFDbkIsTUFBTSxNQUFNLFNBQUcsT0FBTyxDQUFDLGFBQWEsMENBQUUsT0FBTyxDQUFDO1FBRTlDLElBQUksTUFBTSxFQUFFO1lBQ1YsTUFBTSxDQUFDLFlBQVksRUFBRSxDQUFDO1NBQ3ZCO0lBQ0gsQ0FBQztJQUVELFNBQVMsWUFBWTs7UUFDbkIsTUFBTSxNQUFNLFNBQUcsT0FBTyxDQUFDLGFBQWEsMENBQUUsT0FBTyxDQUFDO1FBRTlDLElBQUksTUFBTSxFQUFFO1lBQ1YsTUFBTSxDQUFDLGNBQWMsSUFBSSxDQUFDLENBQUM7WUFDM0IsTUFBTSxDQUFDLGNBQWMsSUFBSSxDQUFDLENBQUM7U0FDNUI7SUFDSCxDQUFDO0FBQ0gsQ0FBQyIsImZpbGUiOiJwYWNrYWdlc19pbWFnZXZpZXdlci1leHRlbnNpb25fbGliX2luZGV4X2pzLV84ZGNhMS45ODY4OTk1ZjI4OTE1MGJkMmU5Yy5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGltYWdldmlld2VyLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYXlvdXRSZXN0b3JlcixcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHsgSUNvbW1hbmRQYWxldHRlLCBXaWRnZXRUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgRG9jdW1lbnRSZWdpc3RyeSwgSURvY3VtZW50V2lkZ2V0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHtcbiAgSUltYWdlVHJhY2tlcixcbiAgSW1hZ2VWaWV3ZXIsXG4gIEltYWdlVmlld2VyRmFjdG9yeVxufSBmcm9tICdAanVweXRlcmxhYi9pbWFnZXZpZXdlcic7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgaW1hZ2Ugd2lkZ2V0IHBsdWdpbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgcmVzZXRJbWFnZSA9ICdpbWFnZXZpZXdlcjpyZXNldC1pbWFnZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHpvb21JbiA9ICdpbWFnZXZpZXdlcjp6b29tLWluJztcblxuICBleHBvcnQgY29uc3Qgem9vbU91dCA9ICdpbWFnZXZpZXdlcjp6b29tLW91dCc7XG5cbiAgZXhwb3J0IGNvbnN0IGZsaXBIb3Jpem9udGFsID0gJ2ltYWdldmlld2VyOmZsaXAtaG9yaXpvbnRhbCc7XG5cbiAgZXhwb3J0IGNvbnN0IGZsaXBWZXJ0aWNhbCA9ICdpbWFnZXZpZXdlcjpmbGlwLXZlcnRpY2FsJztcblxuICBleHBvcnQgY29uc3Qgcm90YXRlQ2xvY2t3aXNlID0gJ2ltYWdldmlld2VyOnJvdGF0ZS1jbG9ja3dpc2UnO1xuXG4gIGV4cG9ydCBjb25zdCByb3RhdGVDb3VudGVyY2xvY2t3aXNlID0gJ2ltYWdldmlld2VyOnJvdGF0ZS1jb3VudGVyY2xvY2t3aXNlJztcblxuICBleHBvcnQgY29uc3QgaW52ZXJ0Q29sb3JzID0gJ2ltYWdldmlld2VyOmludmVydC1jb2xvcnMnO1xufVxuXG4vKipcbiAqIFRoZSBsaXN0IG9mIGZpbGUgdHlwZXMgZm9yIGltYWdlcy5cbiAqL1xuY29uc3QgRklMRV9UWVBFUyA9IFsncG5nJywgJ2dpZicsICdqcGVnJywgJ2JtcCcsICdpY28nLCAndGlmZiddO1xuXG4vKipcbiAqIFRoZSBuYW1lIG9mIHRoZSBmYWN0b3J5IHRoYXQgY3JlYXRlcyBpbWFnZSB3aWRnZXRzLlxuICovXG5jb25zdCBGQUNUT1JZID0gJ0ltYWdlJztcblxuLyoqXG4gKiBUaGUgbmFtZSBvZiB0aGUgZmFjdG9yeSB0aGF0IGNyZWF0ZXMgaW1hZ2Ugd2lkZ2V0cy5cbiAqL1xuY29uc3QgVEVYVF9GQUNUT1JZID0gJ0ltYWdlIChUZXh0KSc7XG5cbi8qKlxuICogVGhlIGxpc3Qgb2YgZmlsZSB0eXBlcyBmb3IgaW1hZ2VzIHdpdGggb3B0aW9uYWwgdGV4dCBtb2Rlcy5cbiAqL1xuY29uc3QgVEVYVF9GSUxFX1RZUEVTID0gWydzdmcnLCAneGJtJ107XG5cbi8qKlxuICogVGhlIHRlc3QgcGF0dGVybiBmb3IgdGV4dCBmaWxlIHR5cGVzIGluIHBhdGhzLlxuICovXG5jb25zdCBURVhUX0ZJTEVfUkVHRVggPSBuZXcgUmVnRXhwKGBbLl0oJHtURVhUX0ZJTEVfVFlQRVMuam9pbignfCcpfSkkYCk7XG5cbi8qKlxuICogVGhlIGltYWdlIGZpbGUgaGFuZGxlciBleHRlbnNpb24uXG4gKi9cbmNvbnN0IHBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPElJbWFnZVRyYWNrZXI+ID0ge1xuICBhY3RpdmF0ZSxcbiAgaWQ6ICdAanVweXRlcmxhYi9pbWFnZXZpZXdlci1leHRlbnNpb246cGx1Z2luJyxcbiAgcHJvdmlkZXM6IElJbWFnZVRyYWNrZXIsXG4gIHJlcXVpcmVzOiBbSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lDb21tYW5kUGFsZXR0ZSwgSUxheW91dFJlc3RvcmVyXSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2luIGFzIGRlZmF1bHQuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbjtcblxuLyoqXG4gKiBBY3RpdmF0ZSB0aGUgaW1hZ2Ugd2lkZ2V0IGV4dGVuc2lvbi5cbiAqL1xuZnVuY3Rpb24gYWN0aXZhdGUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGxcbik6IElJbWFnZVRyYWNrZXIge1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICBjb25zdCBuYW1lc3BhY2UgPSAnaW1hZ2Utd2lkZ2V0JztcblxuICBmdW5jdGlvbiBvbldpZGdldENyZWF0ZWQoXG4gICAgc2VuZGVyOiBhbnksXG4gICAgd2lkZ2V0OiBJRG9jdW1lbnRXaWRnZXQ8SW1hZ2VWaWV3ZXIsIERvY3VtZW50UmVnaXN0cnkuSU1vZGVsPlxuICApIHtcbiAgICAvLyBOb3RpZnkgdGhlIHdpZGdldCB0cmFja2VyIGlmIHJlc3RvcmUgZGF0YSBuZWVkcyB0byB1cGRhdGUuXG4gICAgd2lkZ2V0LmNvbnRleHQucGF0aENoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICB2b2lkIHRyYWNrZXIuc2F2ZSh3aWRnZXQpO1xuICAgIH0pO1xuICAgIHZvaWQgdHJhY2tlci5hZGQod2lkZ2V0KTtcblxuICAgIGNvbnN0IHR5cGVzID0gYXBwLmRvY1JlZ2lzdHJ5LmdldEZpbGVUeXBlc0ZvclBhdGgod2lkZ2V0LmNvbnRleHQucGF0aCk7XG5cbiAgICBpZiAodHlwZXMubGVuZ3RoID4gMCkge1xuICAgICAgd2lkZ2V0LnRpdGxlLmljb24gPSB0eXBlc1swXS5pY29uITtcbiAgICAgIHdpZGdldC50aXRsZS5pY29uQ2xhc3MgPSB0eXBlc1swXS5pY29uQ2xhc3MgPz8gJyc7XG4gICAgICB3aWRnZXQudGl0bGUuaWNvbkxhYmVsID0gdHlwZXNbMF0uaWNvbkxhYmVsID8/ICcnO1xuICAgIH1cbiAgfVxuXG4gIGNvbnN0IGZhY3RvcnkgPSBuZXcgSW1hZ2VWaWV3ZXJGYWN0b3J5KHtcbiAgICBuYW1lOiBGQUNUT1JZLFxuICAgIG1vZGVsTmFtZTogJ2Jhc2U2NCcsXG4gICAgZmlsZVR5cGVzOiBbLi4uRklMRV9UWVBFUywgLi4uVEVYVF9GSUxFX1RZUEVTXSxcbiAgICBkZWZhdWx0Rm9yOiBGSUxFX1RZUEVTLFxuICAgIHJlYWRPbmx5OiB0cnVlXG4gIH0pO1xuXG4gIGNvbnN0IHRleHRGYWN0b3J5ID0gbmV3IEltYWdlVmlld2VyRmFjdG9yeSh7XG4gICAgbmFtZTogVEVYVF9GQUNUT1JZLFxuICAgIG1vZGVsTmFtZTogJ3RleHQnLFxuICAgIGZpbGVUeXBlczogVEVYVF9GSUxFX1RZUEVTLFxuICAgIGRlZmF1bHRGb3I6IFRFWFRfRklMRV9UWVBFUyxcbiAgICByZWFkT25seTogdHJ1ZVxuICB9KTtcblxuICBbZmFjdG9yeSwgdGV4dEZhY3RvcnldLmZvckVhY2goZmFjdG9yeSA9PiB7XG4gICAgYXBwLmRvY1JlZ2lzdHJ5LmFkZFdpZGdldEZhY3RvcnkoZmFjdG9yeSk7XG4gICAgZmFjdG9yeS53aWRnZXRDcmVhdGVkLmNvbm5lY3Qob25XaWRnZXRDcmVhdGVkKTtcbiAgfSk7XG5cbiAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxJbWFnZVZpZXdlcj4+KHtcbiAgICBuYW1lc3BhY2VcbiAgfSk7XG5cbiAgaWYgKHJlc3RvcmVyKSB7XG4gICAgLy8gSGFuZGxlIHN0YXRlIHJlc3RvcmF0aW9uLlxuICAgIHZvaWQgcmVzdG9yZXIucmVzdG9yZSh0cmFja2VyLCB7XG4gICAgICBjb21tYW5kOiAnZG9jbWFuYWdlcjpvcGVuJyxcbiAgICAgIGFyZ3M6IHdpZGdldCA9PiAoe1xuICAgICAgICBwYXRoOiB3aWRnZXQuY29udGV4dC5wYXRoLFxuICAgICAgICBmYWN0b3J5OiBURVhUX0ZJTEVfUkVHRVgudGVzdCh3aWRnZXQuY29udGV4dC5wYXRoKVxuICAgICAgICAgID8gVEVYVF9GQUNUT1JZXG4gICAgICAgICAgOiBGQUNUT1JZXG4gICAgICB9KSxcbiAgICAgIG5hbWU6IHdpZGdldCA9PiB3aWRnZXQuY29udGV4dC5wYXRoXG4gICAgfSk7XG4gIH1cblxuICBhZGRDb21tYW5kcyhhcHAsIHRyYWNrZXIsIHRyYW5zbGF0b3IpO1xuXG4gIGlmIChwYWxldHRlKSB7XG4gICAgY29uc3QgY2F0ZWdvcnkgPSB0cmFucy5fXygnSW1hZ2UgVmlld2VyJyk7XG4gICAgW1xuICAgICAgQ29tbWFuZElEcy56b29tSW4sXG4gICAgICBDb21tYW5kSURzLnpvb21PdXQsXG4gICAgICBDb21tYW5kSURzLnJlc2V0SW1hZ2UsXG4gICAgICBDb21tYW5kSURzLnJvdGF0ZUNsb2Nrd2lzZSxcbiAgICAgIENvbW1hbmRJRHMucm90YXRlQ291bnRlcmNsb2Nrd2lzZSxcbiAgICAgIENvbW1hbmRJRHMuZmxpcEhvcml6b250YWwsXG4gICAgICBDb21tYW5kSURzLmZsaXBWZXJ0aWNhbCxcbiAgICAgIENvbW1hbmRJRHMuaW52ZXJ0Q29sb3JzXG4gICAgXS5mb3JFYWNoKGNvbW1hbmQgPT4ge1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHsgY29tbWFuZCwgY2F0ZWdvcnkgfSk7XG4gICAgfSk7XG4gIH1cblxuICByZXR1cm4gdHJhY2tlcjtcbn1cblxuLyoqXG4gKiBBZGQgdGhlIGNvbW1hbmRzIGZvciB0aGUgaW1hZ2Ugd2lkZ2V0LlxuICovXG5leHBvcnQgZnVuY3Rpb24gYWRkQ29tbWFuZHMoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICB0cmFja2VyOiBJSW1hZ2VUcmFja2VyLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuKSB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IHsgY29tbWFuZHMsIHNoZWxsIH0gPSBhcHA7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlcmUgaXMgYW4gYWN0aXZlIGltYWdlIHZpZXdlci5cbiAgICovXG4gIGZ1bmN0aW9uIGlzRW5hYmxlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gKFxuICAgICAgdHJhY2tlci5jdXJyZW50V2lkZ2V0ICE9PSBudWxsICYmXG4gICAgICB0cmFja2VyLmN1cnJlbnRXaWRnZXQgPT09IHNoZWxsLmN1cnJlbnRXaWRnZXRcbiAgICApO1xuICB9XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZCgnaW1hZ2V2aWV3ZXI6em9vbS1pbicsIHtcbiAgICBleGVjdXRlOiB6b29tSW4sXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdab29tIEluJyksXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoJ2ltYWdldmlld2VyOnpvb20tb3V0Jywge1xuICAgIGV4ZWN1dGU6IHpvb21PdXQsXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdab29tIE91dCcpLFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKCdpbWFnZXZpZXdlcjpyZXNldC1pbWFnZScsIHtcbiAgICBleGVjdXRlOiByZXNldEltYWdlLFxuICAgIGxhYmVsOiB0cmFucy5fXygnUmVzZXQgSW1hZ2UnKSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZCgnaW1hZ2V2aWV3ZXI6cm90YXRlLWNsb2Nrd2lzZScsIHtcbiAgICBleGVjdXRlOiByb3RhdGVDbG9ja3dpc2UsXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdSb3RhdGUgQ2xvY2t3aXNlJyksXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoJ2ltYWdldmlld2VyOnJvdGF0ZS1jb3VudGVyY2xvY2t3aXNlJywge1xuICAgIGV4ZWN1dGU6IHJvdGF0ZUNvdW50ZXJjbG9ja3dpc2UsXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdSb3RhdGUgQ291bnRlcmNsb2Nrd2lzZScpLFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKCdpbWFnZXZpZXdlcjpmbGlwLWhvcml6b250YWwnLCB7XG4gICAgZXhlY3V0ZTogZmxpcEhvcml6b250YWwsXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdGbGlwIGltYWdlIGhvcml6b250YWxseScpLFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKCdpbWFnZXZpZXdlcjpmbGlwLXZlcnRpY2FsJywge1xuICAgIGV4ZWN1dGU6IGZsaXBWZXJ0aWNhbCxcbiAgICBsYWJlbDogdHJhbnMuX18oJ0ZsaXAgaW1hZ2UgdmVydGljYWxseScpLFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKCdpbWFnZXZpZXdlcjppbnZlcnQtY29sb3JzJywge1xuICAgIGV4ZWN1dGU6IGludmVydENvbG9ycyxcbiAgICBsYWJlbDogdHJhbnMuX18oJ0ludmVydCBDb2xvcnMnKSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgZnVuY3Rpb24gem9vbUluKCk6IHZvaWQge1xuICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudDtcblxuICAgIGlmICh3aWRnZXQpIHtcbiAgICAgIHdpZGdldC5zY2FsZSA9IHdpZGdldC5zY2FsZSA+IDEgPyB3aWRnZXQuc2NhbGUgKyAwLjUgOiB3aWRnZXQuc2NhbGUgKiAyO1xuICAgIH1cbiAgfVxuXG4gIGZ1bmN0aW9uIHpvb21PdXQoKTogdm9pZCB7XG4gICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50O1xuXG4gICAgaWYgKHdpZGdldCkge1xuICAgICAgd2lkZ2V0LnNjYWxlID0gd2lkZ2V0LnNjYWxlID4gMSA/IHdpZGdldC5zY2FsZSAtIDAuNSA6IHdpZGdldC5zY2FsZSAvIDI7XG4gICAgfVxuICB9XG5cbiAgZnVuY3Rpb24gcmVzZXRJbWFnZSgpOiB2b2lkIHtcbiAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICBpZiAod2lkZ2V0KSB7XG4gICAgICB3aWRnZXQuc2NhbGUgPSAxO1xuICAgICAgd2lkZ2V0LmNvbG9yaW52ZXJzaW9uID0gMDtcbiAgICAgIHdpZGdldC5yZXNldFJvdGF0aW9uRmxpcCgpO1xuICAgIH1cbiAgfVxuXG4gIGZ1bmN0aW9uIHJvdGF0ZUNsb2Nrd2lzZSgpOiB2b2lkIHtcbiAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICBpZiAod2lkZ2V0KSB7XG4gICAgICB3aWRnZXQucm90YXRlQ2xvY2t3aXNlKCk7XG4gICAgfVxuICB9XG5cbiAgZnVuY3Rpb24gcm90YXRlQ291bnRlcmNsb2Nrd2lzZSgpOiB2b2lkIHtcbiAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICBpZiAod2lkZ2V0KSB7XG4gICAgICB3aWRnZXQucm90YXRlQ291bnRlcmNsb2Nrd2lzZSgpO1xuICAgIH1cbiAgfVxuXG4gIGZ1bmN0aW9uIGZsaXBIb3Jpem9udGFsKCk6IHZvaWQge1xuICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudDtcblxuICAgIGlmICh3aWRnZXQpIHtcbiAgICAgIHdpZGdldC5mbGlwSG9yaXpvbnRhbCgpO1xuICAgIH1cbiAgfVxuXG4gIGZ1bmN0aW9uIGZsaXBWZXJ0aWNhbCgpOiB2b2lkIHtcbiAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICBpZiAod2lkZ2V0KSB7XG4gICAgICB3aWRnZXQuZmxpcFZlcnRpY2FsKCk7XG4gICAgfVxuICB9XG5cbiAgZnVuY3Rpb24gaW52ZXJ0Q29sb3JzKCk6IHZvaWQge1xuICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudDtcblxuICAgIGlmICh3aWRnZXQpIHtcbiAgICAgIHdpZGdldC5jb2xvcmludmVyc2lvbiArPSAxO1xuICAgICAgd2lkZ2V0LmNvbG9yaW52ZXJzaW9uICU9IDI7XG4gICAgfVxuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9