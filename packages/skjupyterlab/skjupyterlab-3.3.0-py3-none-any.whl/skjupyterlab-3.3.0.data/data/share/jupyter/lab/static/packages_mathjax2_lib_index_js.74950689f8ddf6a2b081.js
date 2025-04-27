(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_mathjax2_lib_index_js"],{

/***/ "../packages/mathjax2/lib/index.js":
/*!*****************************************!*\
  !*** ../packages/mathjax2/lib/index.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MathJaxTypesetter": () => (/* binding */ MathJaxTypesetter)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module mathjax2
 */

/**
 * The MathJax Typesetter.
 */
class MathJaxTypesetter {
    /**
     * Create a new MathJax typesetter.
     */
    constructor(options) {
        this._initPromise = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        this._initialized = false;
        this._url = options.url;
        this._config = options.config;
    }
    /**
     * Typeset the math in a node.
     *
     * #### Notes
     * MathJax schedules the typesetting asynchronously,
     * but there are not currently any callbacks or Promises
     * firing when it is done.
     */
    typeset(node) {
        if (!this._initialized) {
            this._init();
        }
        void this._initPromise.promise.then(() => {
            MathJax.Hub.Queue(['Typeset', MathJax.Hub, node]);
            try {
                MathJax.Hub.Queue(['Require', MathJax.Ajax, '[MathJax]/extensions/TeX/AMSmath.js'], () => {
                    MathJax.InputJax.TeX.resetEquationNumbers();
                });
            }
            catch (e) {
                console.error('Error queueing resetEquationNumbers:', e);
            }
        });
    }
    /**
     * Initialize MathJax.
     */
    _init() {
        const head = document.getElementsByTagName('head')[0];
        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = `${this._url}?config=${this._config}&amp;delayStartupUntil=configured`;
        script.charset = 'utf-8';
        head.appendChild(script);
        script.addEventListener('load', () => {
            this._onLoad();
        });
        this._initialized = true;
    }
    /**
     * Handle MathJax loading.
     */
    _onLoad() {
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [
                    ['$', '$'],
                    ['\\(', '\\)']
                ],
                displayMath: [
                    ['$$', '$$'],
                    ['\\[', '\\]']
                ],
                processEscapes: true,
                processEnvironments: true
            },
            // Center justify equations in code and markdown cells. Elsewhere
            // we use CSS to left justify single line equations in code cells.
            displayAlign: 'center',
            CommonHTML: {
                linebreaks: { automatic: true }
            },
            'HTML-CSS': {
                availableFonts: [],
                imageFont: null,
                preferredFont: null,
                webFont: 'STIX-Web',
                styles: { '.MathJax_Display': { margin: 0 } },
                linebreaks: { automatic: true }
            },
            skipStartupTypeset: true,
            messageStyle: 'none'
        });
        MathJax.Hub.Configured();
        this._initPromise.resolve(void 0);
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWF0aGpheDIvc3JjL2luZGV4LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7OztBQUFBOzs7K0VBRytFO0FBQy9FOzs7R0FHRztBQUdpRDtBQUtwRDs7R0FFRztBQUNJLE1BQU0saUJBQWlCO0lBQzVCOztPQUVHO0lBQ0gsWUFBWSxPQUFtQztRQXNGdkMsaUJBQVksR0FBRyxJQUFJLDhEQUFlLEVBQVEsQ0FBQztRQUMzQyxpQkFBWSxHQUFHLEtBQUssQ0FBQztRQXRGM0IsSUFBSSxDQUFDLElBQUksR0FBRyxPQUFPLENBQUMsR0FBRyxDQUFDO1FBQ3hCLElBQUksQ0FBQyxPQUFPLEdBQUcsT0FBTyxDQUFDLE1BQU0sQ0FBQztJQUNoQyxDQUFDO0lBRUQ7Ozs7Ozs7T0FPRztJQUNILE9BQU8sQ0FBQyxJQUFpQjtRQUN2QixJQUFJLENBQUMsSUFBSSxDQUFDLFlBQVksRUFBRTtZQUN0QixJQUFJLENBQUMsS0FBSyxFQUFFLENBQUM7U0FDZDtRQUNELEtBQUssSUFBSSxDQUFDLFlBQVksQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLEdBQUcsRUFBRTtZQUN2QyxPQUFPLENBQUMsR0FBRyxDQUFDLEtBQUssQ0FBQyxDQUFDLFNBQVMsRUFBRSxPQUFPLENBQUMsR0FBRyxFQUFFLElBQUksQ0FBQyxDQUFDLENBQUM7WUFDbEQsSUFBSTtnQkFDRixPQUFPLENBQUMsR0FBRyxDQUFDLEtBQUssQ0FDZixDQUFDLFNBQVMsRUFBRSxPQUFPLENBQUMsSUFBSSxFQUFFLHFDQUFxQyxDQUFDLEVBQ2hFLEdBQUcsRUFBRTtvQkFDSCxPQUFPLENBQUMsUUFBUSxDQUFDLEdBQUcsQ0FBQyxvQkFBb0IsRUFBRSxDQUFDO2dCQUM5QyxDQUFDLENBQ0YsQ0FBQzthQUNIO1lBQUMsT0FBTyxDQUFDLEVBQUU7Z0JBQ1YsT0FBTyxDQUFDLEtBQUssQ0FBQyxzQ0FBc0MsRUFBRSxDQUFDLENBQUMsQ0FBQzthQUMxRDtRQUNILENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUVEOztPQUVHO0lBQ0ssS0FBSztRQUNYLE1BQU0sSUFBSSxHQUFHLFFBQVEsQ0FBQyxvQkFBb0IsQ0FBQyxNQUFNLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQztRQUN0RCxNQUFNLE1BQU0sR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLFFBQVEsQ0FBQyxDQUFDO1FBQ2hELE1BQU0sQ0FBQyxJQUFJLEdBQUcsaUJBQWlCLENBQUM7UUFDaEMsTUFBTSxDQUFDLEdBQUcsR0FBRyxHQUFHLElBQUksQ0FBQyxJQUFJLFdBQVcsSUFBSSxDQUFDLE9BQU8sbUNBQW1DLENBQUM7UUFDcEYsTUFBTSxDQUFDLE9BQU8sR0FBRyxPQUFPLENBQUM7UUFDekIsSUFBSSxDQUFDLFdBQVcsQ0FBQyxNQUFNLENBQUMsQ0FBQztRQUN6QixNQUFNLENBQUMsZ0JBQWdCLENBQUMsTUFBTSxFQUFFLEdBQUcsRUFBRTtZQUNuQyxJQUFJLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDakIsQ0FBQyxDQUFDLENBQUM7UUFDSCxJQUFJLENBQUMsWUFBWSxHQUFHLElBQUksQ0FBQztJQUMzQixDQUFDO0lBRUQ7O09BRUc7SUFDSyxPQUFPO1FBQ2IsT0FBTyxDQUFDLEdBQUcsQ0FBQyxNQUFNLENBQUM7WUFDakIsT0FBTyxFQUFFO2dCQUNQLFVBQVUsRUFBRTtvQkFDVixDQUFDLEdBQUcsRUFBRSxHQUFHLENBQUM7b0JBQ1YsQ0FBQyxLQUFLLEVBQUUsS0FBSyxDQUFDO2lCQUNmO2dCQUNELFdBQVcsRUFBRTtvQkFDWCxDQUFDLElBQUksRUFBRSxJQUFJLENBQUM7b0JBQ1osQ0FBQyxLQUFLLEVBQUUsS0FBSyxDQUFDO2lCQUNmO2dCQUNELGNBQWMsRUFBRSxJQUFJO2dCQUNwQixtQkFBbUIsRUFBRSxJQUFJO2FBQzFCO1lBQ0QsaUVBQWlFO1lBQ2pFLGtFQUFrRTtZQUNsRSxZQUFZLEVBQUUsUUFBUTtZQUN0QixVQUFVLEVBQUU7Z0JBQ1YsVUFBVSxFQUFFLEVBQUUsU0FBUyxFQUFFLElBQUksRUFBRTthQUNoQztZQUNELFVBQVUsRUFBRTtnQkFDVixjQUFjLEVBQUUsRUFBRTtnQkFDbEIsU0FBUyxFQUFFLElBQUk7Z0JBQ2YsYUFBYSxFQUFFLElBQUk7Z0JBQ25CLE9BQU8sRUFBRSxVQUFVO2dCQUNuQixNQUFNLEVBQUUsRUFBRSxrQkFBa0IsRUFBRSxFQUFFLE1BQU0sRUFBRSxDQUFDLEVBQUUsRUFBRTtnQkFDN0MsVUFBVSxFQUFFLEVBQUUsU0FBUyxFQUFFLElBQUksRUFBRTthQUNoQztZQUNELGtCQUFrQixFQUFFLElBQUk7WUFDeEIsWUFBWSxFQUFFLE1BQU07U0FDckIsQ0FBQyxDQUFDO1FBQ0gsT0FBTyxDQUFDLEdBQUcsQ0FBQyxVQUFVLEVBQUUsQ0FBQztRQUN6QixJQUFJLENBQUMsWUFBWSxDQUFDLE9BQU8sQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDO0lBQ3BDLENBQUM7Q0FNRiIsImZpbGUiOiJwYWNrYWdlc19tYXRoamF4Ml9saWJfaW5kZXhfanMuNzQ5NTA2ODlmOGRkZjZhMmIwODEuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIG1hdGhqYXgyXG4gKi9cblxuaW1wb3J0IHsgSVJlbmRlck1pbWUgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lLWludGVyZmFjZXMnO1xuaW1wb3J0IHsgUHJvbWlzZURlbGVnYXRlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuXG4vLyBTdHViIGZvciB3aW5kb3cgTWF0aEpheC5cbmRlY2xhcmUgbGV0IE1hdGhKYXg6IGFueTtcblxuLyoqXG4gKiBUaGUgTWF0aEpheCBUeXBlc2V0dGVyLlxuICovXG5leHBvcnQgY2xhc3MgTWF0aEpheFR5cGVzZXR0ZXIgaW1wbGVtZW50cyBJUmVuZGVyTWltZS5JTGF0ZXhUeXBlc2V0dGVyIHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBNYXRoSmF4IHR5cGVzZXR0ZXIuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBNYXRoSmF4VHlwZXNldHRlci5JT3B0aW9ucykge1xuICAgIHRoaXMuX3VybCA9IG9wdGlvbnMudXJsO1xuICAgIHRoaXMuX2NvbmZpZyA9IG9wdGlvbnMuY29uZmlnO1xuICB9XG5cbiAgLyoqXG4gICAqIFR5cGVzZXQgdGhlIG1hdGggaW4gYSBub2RlLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIE1hdGhKYXggc2NoZWR1bGVzIHRoZSB0eXBlc2V0dGluZyBhc3luY2hyb25vdXNseSxcbiAgICogYnV0IHRoZXJlIGFyZSBub3QgY3VycmVudGx5IGFueSBjYWxsYmFja3Mgb3IgUHJvbWlzZXNcbiAgICogZmlyaW5nIHdoZW4gaXQgaXMgZG9uZS5cbiAgICovXG4gIHR5cGVzZXQobm9kZTogSFRNTEVsZW1lbnQpOiB2b2lkIHtcbiAgICBpZiAoIXRoaXMuX2luaXRpYWxpemVkKSB7XG4gICAgICB0aGlzLl9pbml0KCk7XG4gICAgfVxuICAgIHZvaWQgdGhpcy5faW5pdFByb21pc2UucHJvbWlzZS50aGVuKCgpID0+IHtcbiAgICAgIE1hdGhKYXguSHViLlF1ZXVlKFsnVHlwZXNldCcsIE1hdGhKYXguSHViLCBub2RlXSk7XG4gICAgICB0cnkge1xuICAgICAgICBNYXRoSmF4Lkh1Yi5RdWV1ZShcbiAgICAgICAgICBbJ1JlcXVpcmUnLCBNYXRoSmF4LkFqYXgsICdbTWF0aEpheF0vZXh0ZW5zaW9ucy9UZVgvQU1TbWF0aC5qcyddLFxuICAgICAgICAgICgpID0+IHtcbiAgICAgICAgICAgIE1hdGhKYXguSW5wdXRKYXguVGVYLnJlc2V0RXF1YXRpb25OdW1iZXJzKCk7XG4gICAgICAgICAgfVxuICAgICAgICApO1xuICAgICAgfSBjYXRjaCAoZSkge1xuICAgICAgICBjb25zb2xlLmVycm9yKCdFcnJvciBxdWV1ZWluZyByZXNldEVxdWF0aW9uTnVtYmVyczonLCBlKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbml0aWFsaXplIE1hdGhKYXguXG4gICAqL1xuICBwcml2YXRlIF9pbml0KCk6IHZvaWQge1xuICAgIGNvbnN0IGhlYWQgPSBkb2N1bWVudC5nZXRFbGVtZW50c0J5VGFnTmFtZSgnaGVhZCcpWzBdO1xuICAgIGNvbnN0IHNjcmlwdCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ3NjcmlwdCcpO1xuICAgIHNjcmlwdC50eXBlID0gJ3RleHQvamF2YXNjcmlwdCc7XG4gICAgc2NyaXB0LnNyYyA9IGAke3RoaXMuX3VybH0/Y29uZmlnPSR7dGhpcy5fY29uZmlnfSZhbXA7ZGVsYXlTdGFydHVwVW50aWw9Y29uZmlndXJlZGA7XG4gICAgc2NyaXB0LmNoYXJzZXQgPSAndXRmLTgnO1xuICAgIGhlYWQuYXBwZW5kQ2hpbGQoc2NyaXB0KTtcbiAgICBzY3JpcHQuYWRkRXZlbnRMaXN0ZW5lcignbG9hZCcsICgpID0+IHtcbiAgICAgIHRoaXMuX29uTG9hZCgpO1xuICAgIH0pO1xuICAgIHRoaXMuX2luaXRpYWxpemVkID0gdHJ1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgTWF0aEpheCBsb2FkaW5nLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25Mb2FkKCk6IHZvaWQge1xuICAgIE1hdGhKYXguSHViLkNvbmZpZyh7XG4gICAgICB0ZXgyamF4OiB7XG4gICAgICAgIGlubGluZU1hdGg6IFtcbiAgICAgICAgICBbJyQnLCAnJCddLFxuICAgICAgICAgIFsnXFxcXCgnLCAnXFxcXCknXVxuICAgICAgICBdLFxuICAgICAgICBkaXNwbGF5TWF0aDogW1xuICAgICAgICAgIFsnJCQnLCAnJCQnXSxcbiAgICAgICAgICBbJ1xcXFxbJywgJ1xcXFxdJ11cbiAgICAgICAgXSxcbiAgICAgICAgcHJvY2Vzc0VzY2FwZXM6IHRydWUsXG4gICAgICAgIHByb2Nlc3NFbnZpcm9ubWVudHM6IHRydWVcbiAgICAgIH0sXG4gICAgICAvLyBDZW50ZXIganVzdGlmeSBlcXVhdGlvbnMgaW4gY29kZSBhbmQgbWFya2Rvd24gY2VsbHMuIEVsc2V3aGVyZVxuICAgICAgLy8gd2UgdXNlIENTUyB0byBsZWZ0IGp1c3RpZnkgc2luZ2xlIGxpbmUgZXF1YXRpb25zIGluIGNvZGUgY2VsbHMuXG4gICAgICBkaXNwbGF5QWxpZ246ICdjZW50ZXInLFxuICAgICAgQ29tbW9uSFRNTDoge1xuICAgICAgICBsaW5lYnJlYWtzOiB7IGF1dG9tYXRpYzogdHJ1ZSB9XG4gICAgICB9LFxuICAgICAgJ0hUTUwtQ1NTJzoge1xuICAgICAgICBhdmFpbGFibGVGb250czogW10sXG4gICAgICAgIGltYWdlRm9udDogbnVsbCxcbiAgICAgICAgcHJlZmVycmVkRm9udDogbnVsbCxcbiAgICAgICAgd2ViRm9udDogJ1NUSVgtV2ViJyxcbiAgICAgICAgc3R5bGVzOiB7ICcuTWF0aEpheF9EaXNwbGF5JzogeyBtYXJnaW46IDAgfSB9LFxuICAgICAgICBsaW5lYnJlYWtzOiB7IGF1dG9tYXRpYzogdHJ1ZSB9XG4gICAgICB9LFxuICAgICAgc2tpcFN0YXJ0dXBUeXBlc2V0OiB0cnVlLFxuICAgICAgbWVzc2FnZVN0eWxlOiAnbm9uZSdcbiAgICB9KTtcbiAgICBNYXRoSmF4Lkh1Yi5Db25maWd1cmVkKCk7XG4gICAgdGhpcy5faW5pdFByb21pc2UucmVzb2x2ZSh2b2lkIDApO1xuICB9XG5cbiAgcHJpdmF0ZSBfaW5pdFByb21pc2UgPSBuZXcgUHJvbWlzZURlbGVnYXRlPHZvaWQ+KCk7XG4gIHByaXZhdGUgX2luaXRpYWxpemVkID0gZmFsc2U7XG4gIHByaXZhdGUgX3VybDogc3RyaW5nO1xuICBwcml2YXRlIF9jb25maWc6IHN0cmluZztcbn1cblxuLyoqXG4gKiBOYW1lc3BhY2UgZm9yIE1hdGhKYXhUeXBlc2V0dGVyLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE1hdGhKYXhUeXBlc2V0dGVyIHtcbiAgLyoqXG4gICAqIE1hdGhKYXhUeXBlc2V0dGVyIGNvbnN0cnVjdG9yIG9wdGlvbnMuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgdXJsIHRvIGxvYWQgTWF0aEpheCBmcm9tLlxuICAgICAqL1xuICAgIHVybDogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogQSBjb25maWd1cmF0aW9uIHN0cmluZyB0byBjb21wb3NlIGludG8gdGhlIE1hdGhKYXggVVJMLlxuICAgICAqL1xuICAgIGNvbmZpZzogc3RyaW5nO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9