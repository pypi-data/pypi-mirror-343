(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_csvviewer_lib_index_js"],{

/***/ "../packages/csvviewer/lib/index.js":
/*!******************************************!*\
  !*** ../packages/csvviewer/lib/index.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DSVModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_0__.DSVModel),
/* harmony export */   "parseDSV": () => (/* reexport safe */ _parse__WEBPACK_IMPORTED_MODULE_1__.parseDSV),
/* harmony export */   "parseDSVNoQuotes": () => (/* reexport safe */ _parse__WEBPACK_IMPORTED_MODULE_1__.parseDSVNoQuotes),
/* harmony export */   "CSVDelimiter": () => (/* reexport safe */ _toolbar__WEBPACK_IMPORTED_MODULE_2__.CSVDelimiter),
/* harmony export */   "CSVDocumentWidget": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_3__.CSVDocumentWidget),
/* harmony export */   "CSVViewer": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_3__.CSVViewer),
/* harmony export */   "CSVViewerFactory": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_3__.CSVViewerFactory),
/* harmony export */   "GridSearchService": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_3__.GridSearchService),
/* harmony export */   "TSVViewerFactory": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_3__.TSVViewerFactory),
/* harmony export */   "TextRenderConfig": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_3__.TextRenderConfig)
/* harmony export */ });
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./model */ "../packages/csvviewer/lib/model.js");
/* harmony import */ var _parse__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./parse */ "../packages/csvviewer/lib/parse.js");
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./toolbar */ "../packages/csvviewer/lib/toolbar.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./widget */ "../packages/csvviewer/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module csvviewer
 */






/***/ }),

/***/ "../packages/csvviewer/lib/model.js":
/*!******************************************!*\
  !*** ../packages/csvviewer/lib/model.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DSVModel": () => (/* binding */ DSVModel)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/datagrid */ "webpack/sharing/consume/default/@lumino/datagrid/@lumino/datagrid");
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _parse__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./parse */ "../packages/csvviewer/lib/parse.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/*
Possible ideas for further implementation:

- Show a spinner or something visible when we are doing delayed parsing.
- The cache right now handles scrolling down great - it gets the next several hundred rows. However, scrolling up causes lots of cache misses - each new row causes a flush of the cache. When invalidating an entire cache, we should put the requested row in middle of the cache (adjusting for rows at the beginning or end). When populating a cache, we should retrieve rows both above and below the requested row.
- When we have a header, and we are guessing the parser to use, try checking just the part of the file *after* the header row for quotes. I think often a first header row is quoted, but the rest of the file is not and can be parsed much faster.
- autdetect the delimiter (look for comma, tab, semicolon in first line. If more than one found, parse first row with comma, tab, semicolon delimiters. One with most fields wins).
- Toolbar buttons to control the row delimiter, the parsing engine (quoted/not quoted), the quote character, etc.
- Investigate incremental loading strategies in the parseAsync function. In initial investigations, setting the chunk size to 100k in parseAsync seems cause instability with large files in Chrome (such as 8-million row files). Perhaps this is because we are recycling the row offset and column offset arrays quickly? It doesn't seem that there is a memory leak. On this theory, perhaps we just need to keep the offsets list an actual list, and pass it into the parsing function to extend without copying, and finalize it into an array buffer only when we are done parsing. Or perhaps we double the size of the array buffer each time, which may be wasteful, but at the end we trim it down if it's too wasteful (perhaps we have our own object that is backed by an array buffer, but has a push method that will automatically double the array buffer size as needed, and a trim function to finalize the array to exactly the size needed)? Or perhaps we don't use array buffers at all - compare the memory cost and speed of keeping the offsets as lists instead of memory buffers.
- Investigate a time-based incremental parsing strategy, rather than a row-based one. The parser could take a maximum time to parse (say 300ms), and will parse up to that duration, in which case the parser probably also needs a way to notify when it has reached the end of a file.
- For very large files, where we are only storing a small cache, scrolling is very laggy in Safari. It would be good to profile it.
*/
/**
 * Possible delimiter-separated data parsers.
 */
const PARSERS = {
    quotes: _parse__WEBPACK_IMPORTED_MODULE_2__.parseDSV,
    noquotes: _parse__WEBPACK_IMPORTED_MODULE_2__.parseDSVNoQuotes
};
/**
 * A data model implementation for in-memory delimiter-separated data.
 *
 * #### Notes
 * This model handles data with up to 2**32 characters.
 */
class DSVModel extends _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__.DataModel {
    /**
     * Create a data model with static CSV data.
     *
     * @param options - The options for initializing the data model.
     */
    constructor(options) {
        super();
        this._rowCount = 0;
        // Cache information
        /**
         * The header strings.
         */
        this._header = [];
        /**
         * The column offset cache, starting with row _columnOffsetsStartingRow
         *
         * #### Notes
         * The index of the first character in the data string for row r, column c is
         * _columnOffsets[(r-this._columnOffsetsStartingRow)*numColumns+c]
         */
        this._columnOffsets = new Uint32Array(0);
        /**
         * The row that _columnOffsets[0] represents.
         */
        this._columnOffsetsStartingRow = 0;
        /**
         * The maximum number of rows to parse when there is a cache miss.
         */
        this._maxCacheGet = 1000;
        /**
         * The index for the start of each row.
         */
        this._rowOffsets = new Uint32Array(0);
        // Bookkeeping variables.
        this._delayedParse = null;
        this._startedParsing = false;
        this._doneParsing = false;
        this._isDisposed = false;
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        let { data, delimiter = ',', rowDelimiter = undefined, quote = '"', quoteParser = undefined, header = true, initialRows = 500 } = options;
        this._rawData = data;
        this._delimiter = delimiter;
        this._quote = quote;
        this._quoteEscaped = new RegExp(quote + quote, 'g');
        this._initialRows = initialRows;
        // Guess the row delimiter if it was not supplied. This will be fooled if a
        // different line delimiter possibility appears in the first row.
        if (rowDelimiter === undefined) {
            const i = data.slice(0, 5000).indexOf('\r');
            if (i === -1) {
                rowDelimiter = '\n';
            }
            else if (data[i + 1] === '\n') {
                rowDelimiter = '\r\n';
            }
            else {
                rowDelimiter = '\r';
            }
        }
        this._rowDelimiter = rowDelimiter;
        if (quoteParser === undefined) {
            // Check for the existence of quotes if the quoteParser is not set.
            quoteParser = data.indexOf(quote) >= 0;
        }
        this._parser = quoteParser ? 'quotes' : 'noquotes';
        // Parse the data.
        this.parseAsync();
        // Cache the header row.
        if (header === true && this._columnCount > 0) {
            const h = [];
            for (let c = 0; c < this._columnCount; c++) {
                h.push(this._getField(0, c));
            }
            this._header = h;
        }
    }
    /**
     * Whether this model has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A promise that resolves when the model has parsed all of its data.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * The string representation of the data.
     */
    get rawData() {
        return this._rawData;
    }
    set rawData(value) {
        this._rawData = value;
    }
    /**
     * The initial chunk of rows to parse.
     */
    get initialRows() {
        return this._initialRows;
    }
    set initialRows(value) {
        this._initialRows = value;
    }
    /**
     * The header strings.
     */
    get header() {
        return this._header;
    }
    set header(value) {
        this._header = value;
    }
    /**
     * The delimiter between entries on the same row.
     */
    get delimiter() {
        return this._delimiter;
    }
    /**
     * The delimiter between rows.
     */
    get rowDelimiter() {
        return this._rowDelimiter;
    }
    /**
     * A boolean determined by whether parsing has completed.
     */
    get doneParsing() {
        return this._doneParsing;
    }
    /**
     * Get the row count for a region in the data model.
     *
     * @param region - The row region of interest.
     *
     * @returns - The row count for the region.
     */
    rowCount(region) {
        if (region === 'body') {
            if (this._header.length === 0) {
                return this._rowCount;
            }
            else {
                return this._rowCount - 1;
            }
        }
        return 1;
    }
    /**
     * Get the column count for a region in the data model.
     *
     * @param region - The column region of interest.
     *
     * @returns - The column count for the region.
     */
    columnCount(region) {
        if (region === 'body') {
            return this._columnCount;
        }
        return 1;
    }
    /**
     * Get the data value for a cell in the data model.
     *
     * @param region - The cell region of interest.
     *
     * @param row - The row index of the cell of interest.
     *
     * @param column - The column index of the cell of interest.
     *
     * @param returns - The data value for the specified cell.
     */
    data(region, row, column) {
        let value;
        // Look up the field and value for the region.
        switch (region) {
            case 'body':
                if (this._header.length === 0) {
                    value = this._getField(row, column);
                }
                else {
                    value = this._getField(row + 1, column);
                }
                break;
            case 'column-header':
                if (this._header.length === 0) {
                    value = (column + 1).toString();
                }
                else {
                    value = this._header[column];
                }
                break;
            case 'row-header':
                value = (row + 1).toString();
                break;
            case 'corner-header':
                value = '';
                break;
            default:
                throw 'unreachable';
        }
        // Return the final value.
        return value;
    }
    /**
     * Dispose the resources held by this model.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._columnCount = undefined;
        this._rowCount = undefined;
        this._rowOffsets = null;
        this._columnOffsets = null;
        this._rawData = null;
        // Clear out state associated with the asynchronous parsing.
        if (this._doneParsing === false) {
            // Explicitly catch this rejection at least once so an error is not thrown
            // to the console.
            this.ready.catch(() => {
                return;
            });
            this._ready.reject(undefined);
        }
        if (this._delayedParse !== null) {
            window.clearTimeout(this._delayedParse);
        }
    }
    /**
     * Get the index in the data string for the first character of a row and
     * column.
     *
     * @param row - The row of the data item.
     * @param column - The column of the data item.
     * @returns - The index into the data string where the data item starts.
     */
    getOffsetIndex(row, column) {
        // Declare local variables.
        const ncols = this._columnCount;
        // Check to see if row *should* be in the cache, based on the cache size.
        let rowIndex = (row - this._columnOffsetsStartingRow) * ncols;
        if (rowIndex < 0 || rowIndex > this._columnOffsets.length) {
            // Row isn't in the cache, so we invalidate the entire cache and set up
            // the cache to hold the requested row.
            this._columnOffsets.fill(0xffffffff);
            this._columnOffsetsStartingRow = row;
            rowIndex = 0;
        }
        // Check to see if we need to fetch the row data into the cache.
        if (this._columnOffsets[rowIndex] === 0xffffffff) {
            // Figure out how many rows below us also need to be fetched.
            let maxRows = 1;
            while (maxRows <= this._maxCacheGet &&
                this._columnOffsets[rowIndex + maxRows * ncols] === 0xffffff) {
                maxRows++;
            }
            // Parse the data to get the column offsets.
            const { offsets } = PARSERS[this._parser]({
                data: this._rawData,
                delimiter: this._delimiter,
                rowDelimiter: this._rowDelimiter,
                quote: this._quote,
                columnOffsets: true,
                maxRows: maxRows,
                ncols: ncols,
                startIndex: this._rowOffsets[row]
            });
            // Copy results to the cache.
            for (let i = 0; i < offsets.length; i++) {
                this._columnOffsets[rowIndex + i] = offsets[i];
            }
        }
        // Return the offset index from cache.
        return this._columnOffsets[rowIndex + column];
    }
    /**
     * Parse the data string asynchronously.
     *
     * #### Notes
     * It can take several seconds to parse a several hundred megabyte string, so
     * we parse the first 500 rows to get something up on the screen, then we
     * parse the full data string asynchronously.
     */
    parseAsync() {
        // Number of rows to get initially.
        let currentRows = this._initialRows;
        // Number of rows to get in each chunk thereafter. We set this high to just
        // get the rest of the rows for now.
        let chunkRows = Math.pow(2, 32) - 1;
        // We give the UI a chance to draw by delaying the chunk parsing.
        const delay = 30; // milliseconds
        // Define a function to parse a chunk up to and including endRow.
        const parseChunk = (endRow) => {
            try {
                this._computeRowOffsets(endRow);
            }
            catch (e) {
                // Sometimes the data string cannot be parsed with the full parser (for
                // example, we may have the wrong delimiter). In these cases, fall back to
                // the simpler parser so we can show something.
                if (this._parser === 'quotes') {
                    console.warn(e);
                    this._parser = 'noquotes';
                    this._resetParser();
                    this._computeRowOffsets(endRow);
                }
                else {
                    throw e;
                }
            }
            return this._doneParsing;
        };
        // Reset the parser to its initial state.
        this._resetParser();
        // Parse the first rows to give us the start of the data right away.
        const done = parseChunk(currentRows);
        // If we are done, return early.
        if (done) {
            return;
        }
        // Define a function to recursively parse the next chunk after a delay.
        const delayedParse = () => {
            // Parse up to the new end row.
            const done = parseChunk(currentRows + chunkRows);
            currentRows += chunkRows;
            // Gradually double the chunk size until we reach a million rows, if we
            // start below a million-row chunk size.
            if (chunkRows < 1000000) {
                chunkRows *= 2;
            }
            // If we aren't done, the schedule another parse.
            if (done) {
                this._delayedParse = null;
            }
            else {
                this._delayedParse = window.setTimeout(delayedParse, delay);
            }
        };
        // Parse full data string in chunks, delayed by a few milliseconds to give the UI a chance to draw.
        this._delayedParse = window.setTimeout(delayedParse, delay);
    }
    /**
     * Compute the row offsets and initialize the column offset cache.
     *
     * @param endRow - The last row to parse, from the start of the data (first
     * row is row 1).
     *
     * #### Notes
     * This method supports parsing the data incrementally by calling it with
     * incrementally higher endRow. Rows that have already been parsed will not be
     * parsed again.
     */
    _computeRowOffsets(endRow = 4294967295) {
        var _a;
        // If we've already parsed up to endRow, or if we've already parsed the
        // entire data set, return early.
        if (this._rowCount >= endRow || this._doneParsing === true) {
            return;
        }
        // Compute the column count if we don't already have it.
        if (this._columnCount === undefined) {
            // Get number of columns in first row
            this._columnCount = PARSERS[this._parser]({
                data: this._rawData,
                delimiter: this._delimiter,
                rowDelimiter: this._rowDelimiter,
                quote: this._quote,
                columnOffsets: true,
                maxRows: 1
            }).ncols;
        }
        // `reparse` is the number of rows we are requesting to parse over again.
        // We generally start at the beginning of the last row offset, so that the
        // first row offset returned is the same as the last row offset we already
        // have. We parse the data up to and including the requested row.
        const reparse = this._rowCount > 0 ? 1 : 0;
        const { nrows, offsets } = PARSERS[this._parser]({
            data: this._rawData,
            startIndex: (_a = this._rowOffsets[this._rowCount - reparse]) !== null && _a !== void 0 ? _a : 0,
            delimiter: this._delimiter,
            rowDelimiter: this._rowDelimiter,
            quote: this._quote,
            columnOffsets: false,
            maxRows: endRow - this._rowCount + reparse
        });
        // If we have already set up our initial bookkeeping, return early if we
        // did not get any new rows beyond the last row that we've parsed, i.e.,
        // nrows===1.
        if (this._startedParsing && nrows <= reparse) {
            this._doneParsing = true;
            this._ready.resolve(undefined);
            return;
        }
        this._startedParsing = true;
        // Update the row count, accounting for how many rows were reparsed.
        const oldRowCount = this._rowCount;
        const duplicateRows = Math.min(nrows, reparse);
        this._rowCount = oldRowCount + nrows - duplicateRows;
        // If we didn't reach the requested row, we must be done.
        if (this._rowCount < endRow) {
            this._doneParsing = true;
            this._ready.resolve(undefined);
        }
        // Copy the new offsets into a new row offset array if needed.
        if (this._rowCount > oldRowCount) {
            const oldRowOffsets = this._rowOffsets;
            this._rowOffsets = new Uint32Array(this._rowCount);
            this._rowOffsets.set(oldRowOffsets);
            this._rowOffsets.set(offsets, oldRowCount - duplicateRows);
        }
        // Expand the column offsets array if needed
        // If the full column offsets array is small enough, build a cache big
        // enough for all column offsets. We allocate up to 128 megabytes:
        // 128*(2**20 bytes/M)/(4 bytes/entry) = 33554432 entries.
        const maxColumnOffsetsRows = Math.floor(33554432 / this._columnCount);
        // We need to expand the column offset array if we were storing all column
        // offsets before. Check to see if the previous size was small enough that
        // we stored all column offsets.
        if (oldRowCount <= maxColumnOffsetsRows) {
            // Check to see if the new column offsets array is small enough to still
            // store, or if we should cut over to a small cache.
            if (this._rowCount <= maxColumnOffsetsRows) {
                // Expand the existing column offset array for new column offsets.
                const oldColumnOffsets = this._columnOffsets;
                this._columnOffsets = new Uint32Array(this._rowCount * this._columnCount);
                this._columnOffsets.set(oldColumnOffsets);
                this._columnOffsets.fill(0xffffffff, oldColumnOffsets.length);
            }
            else {
                // If not, then our cache size is at most the maximum number of rows we
                // fill in the cache at a time.
                const oldColumnOffsets = this._columnOffsets;
                this._columnOffsets = new Uint32Array(Math.min(this._maxCacheGet, maxColumnOffsetsRows) * this._columnCount);
                // Fill in the entries we already have.
                this._columnOffsets.set(oldColumnOffsets.subarray(0, this._columnOffsets.length));
                // Invalidate the rest of the entries.
                this._columnOffsets.fill(0xffffffff, oldColumnOffsets.length);
                this._columnOffsetsStartingRow = 0;
            }
        }
        // We have more rows than before, so emit the rows-inserted change signal.
        let firstIndex = oldRowCount;
        if (this._header.length > 0) {
            firstIndex -= 1;
        }
        this.emitChanged({
            type: 'rows-inserted',
            region: 'body',
            index: firstIndex,
            span: this._rowCount - oldRowCount
        });
    }
    /**
     * Get the parsed string field for a row and column.
     *
     * @param row - The row number of the data item.
     * @param column - The column number of the data item.
     * @returns The parsed string for the data item.
     */
    _getField(row, column) {
        // Declare local variables.
        let value;
        let nextIndex;
        // Find the index for the first character in the field.
        const index = this.getOffsetIndex(row, column);
        // Initialize the trim adjustments.
        let trimRight = 0;
        let trimLeft = 0;
        // Find the end of the slice (the start of the next field), and how much we
        // should adjust to trim off a trailing field or row delimiter. First check
        // if we are getting the last column.
        if (column === this._columnCount - 1) {
            // Check if we are getting any row but the last.
            if (row < this._rowCount - 1) {
                // Set the next offset to the next row, column 0.
                nextIndex = this.getOffsetIndex(row + 1, 0);
                // Since we are not at the last row, we need to trim off the row
                // delimiter.
                trimRight += this._rowDelimiter.length;
            }
            else {
                // We are getting the last data item, so the slice end is the end of the
                // data string.
                nextIndex = this._rawData.length;
                // The string may or may not end in a row delimiter (RFC 4180 2.2), so
                // we explicitly check if we should trim off a row delimiter.
                if (this._rawData[nextIndex - 1] ===
                    this._rowDelimiter[this._rowDelimiter.length - 1]) {
                    trimRight += this._rowDelimiter.length;
                }
            }
        }
        else {
            // The next field starts at the next column offset.
            nextIndex = this.getOffsetIndex(row, column + 1);
            // Trim off the delimiter if it exists at the end of the field
            if (index < nextIndex &&
                this._rawData[nextIndex - 1] === this._delimiter) {
                trimRight += 1;
            }
        }
        // Check to see if the field begins with a quote. If it does, trim a quote on either side.
        if (this._rawData[index] === this._quote) {
            trimLeft += 1;
            trimRight += 1;
        }
        // Slice the actual value out of the data string.
        value = this._rawData.slice(index + trimLeft, nextIndex - trimRight);
        // If we have a quoted field and we have an escaped quote inside it, unescape it.
        if (trimLeft === 1 && value.indexOf(this._quote) !== -1) {
            value = value.replace(this._quoteEscaped, this._quote);
        }
        // Return the value.
        return value;
    }
    /**
     * Reset the parser state.
     */
    _resetParser() {
        this._columnCount = undefined;
        this._rowOffsets = new Uint32Array(0);
        this._rowCount = 0;
        this._startedParsing = false;
        this._columnOffsets = new Uint32Array(0);
        // Clear out state associated with the asynchronous parsing.
        if (this._doneParsing === false) {
            // Explicitly catch this rejection at least once so an error is not thrown
            // to the console.
            this.ready.catch(() => {
                return;
            });
            this._ready.reject(undefined);
        }
        this._doneParsing = false;
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        if (this._delayedParse !== null) {
            window.clearTimeout(this._delayedParse);
            this._delayedParse = null;
        }
        this.emitChanged({ type: 'model-reset' });
    }
}


/***/ }),

/***/ "../packages/csvviewer/lib/parse.js":
/*!******************************************!*\
  !*** ../packages/csvviewer/lib/parse.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "parseDSV": () => (/* binding */ parseDSV),
/* harmony export */   "parseDSVNoQuotes": () => (/* binding */ parseDSVNoQuotes)
/* harmony export */ });
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * Possible parser states.
 */
var STATE;
(function (STATE) {
    STATE[STATE["QUOTED_FIELD"] = 0] = "QUOTED_FIELD";
    STATE[STATE["QUOTED_FIELD_QUOTE"] = 1] = "QUOTED_FIELD_QUOTE";
    STATE[STATE["UNQUOTED_FIELD"] = 2] = "UNQUOTED_FIELD";
    STATE[STATE["NEW_FIELD"] = 3] = "NEW_FIELD";
    STATE[STATE["NEW_ROW"] = 4] = "NEW_ROW";
})(STATE || (STATE = {}));
/**
 * Possible row delimiters for the parser.
 */
var ROW_DELIMITER;
(function (ROW_DELIMITER) {
    ROW_DELIMITER[ROW_DELIMITER["CR"] = 0] = "CR";
    ROW_DELIMITER[ROW_DELIMITER["CRLF"] = 1] = "CRLF";
    ROW_DELIMITER[ROW_DELIMITER["LF"] = 2] = "LF";
})(ROW_DELIMITER || (ROW_DELIMITER = {}));
/**
 * Parse delimiter-separated data.
 *
 * @param options: The parser options
 * @returns An object giving the offsets for the rows or columns parsed.
 *
 * #### Notes
 * This implementation is based on [RFC 4180](https://tools.ietf.org/html/rfc4180).
 */
function parseDSV(options) {
    const { data, columnOffsets, delimiter = ',', startIndex = 0, maxRows = 0xffffffff, rowDelimiter = '\r\n', quote = '"' } = options;
    // ncols will be set automatically if it is undefined.
    let ncols = options.ncols;
    // The number of rows we've already parsed.
    let nrows = 0;
    // The row or column offsets we return.
    const offsets = [];
    // Set up some useful local variables.
    const CH_DELIMITER = delimiter.charCodeAt(0);
    const CH_QUOTE = quote.charCodeAt(0);
    const CH_LF = 10; // \n
    const CH_CR = 13; // \r
    const endIndex = data.length;
    const { QUOTED_FIELD, QUOTED_FIELD_QUOTE, UNQUOTED_FIELD, NEW_FIELD, NEW_ROW } = STATE;
    const { CR, LF, CRLF } = ROW_DELIMITER;
    const [rowDelimiterCode, rowDelimiterLength] = rowDelimiter === '\r\n'
        ? [CRLF, 2]
        : rowDelimiter === '\r'
            ? [CR, 1]
            : [LF, 1];
    // Always start off at the beginning of a row.
    let state = NEW_ROW;
    // Set up the starting index.
    let i = startIndex;
    // We initialize to 0 just in case we are asked to parse past the end of the
    // string. In that case, we want the number of columns to be 0.
    let col = 0;
    // Declare some useful temporaries
    let char;
    // Loop through the data string
    while (i < endIndex) {
        // i is the index of a character in the state.
        // If we just hit a new row, and there are still characters left, push a new
        // offset on and reset the column counter. We want this logic at the top of
        // the while loop rather than the bottom because we don't want a trailing
        // row delimiter at the end of the data to trigger a new row offset.
        if (state === NEW_ROW) {
            // Start a new row and reset the column counter.
            offsets.push(i);
            col = 1;
        }
        // Below, we handle this character, modify the parser state and increment the index to be consistent.
        // Get the integer code for the current character, so the comparisons below
        // are faster.
        char = data.charCodeAt(i);
        // Update the parser state. This switch statement is responsible for
        // updating the state to be consistent with the index i+1 (we increment i
        // after the switch statement). In some situations, we may increment i
        // inside this loop to skip over indices as a shortcut.
        switch (state) {
            // At the beginning of a row or field, we can have a quote, row delimiter, or field delimiter.
            case NEW_ROW:
            case NEW_FIELD:
                switch (char) {
                    // If we have a quote, we are starting an escaped field.
                    case CH_QUOTE:
                        state = QUOTED_FIELD;
                        break;
                    // A field delimiter means we are starting a new field.
                    case CH_DELIMITER:
                        state = NEW_FIELD;
                        break;
                    // A row delimiter means we are starting a new row.
                    case CH_CR:
                        if (rowDelimiterCode === CR) {
                            state = NEW_ROW;
                        }
                        else if (rowDelimiterCode === CRLF &&
                            data.charCodeAt(i + 1) === CH_LF) {
                            // If we see an expected \r\n, then increment to the end of the delimiter.
                            i++;
                            state = NEW_ROW;
                        }
                        else {
                            throw `string index ${i} (in row ${nrows}, column ${col}): carriage return found, but not as part of a row delimiter C ${data.charCodeAt(i + 1)}`;
                        }
                        break;
                    case CH_LF:
                        if (rowDelimiterCode === LF) {
                            state = NEW_ROW;
                        }
                        else {
                            throw `string index ${i} (in row ${nrows}, column ${col}): line feed found, but row delimiter starts with a carriage return`;
                        }
                        break;
                    // Otherwise, we are starting an unquoted field.
                    default:
                        state = UNQUOTED_FIELD;
                        break;
                }
                break;
            // We are in a quoted field.
            case QUOTED_FIELD:
                // Skip ahead until we see another quote, which either ends the quoted
                // field or starts an escaped quote.
                i = data.indexOf(quote, i);
                if (i < 0) {
                    throw `string index ${i} (in row ${nrows}, column ${col}): mismatched quote`;
                }
                state = QUOTED_FIELD_QUOTE;
                break;
            // We just saw a quote in a quoted field. This could be the end of the
            // field, or it could be a repeated quote (i.e., an escaped quote according
            // to RFC 4180).
            case QUOTED_FIELD_QUOTE:
                switch (char) {
                    // Another quote means we just saw an escaped quote, so we are still in
                    // the quoted field.
                    case CH_QUOTE:
                        state = QUOTED_FIELD;
                        break;
                    // A field or row delimiter means the quoted field just ended and we are
                    // going into a new field or new row.
                    case CH_DELIMITER:
                        state = NEW_FIELD;
                        break;
                    // A row delimiter means we are starting a new row in the next index.
                    case CH_CR:
                        if (rowDelimiterCode === CR) {
                            state = NEW_ROW;
                        }
                        else if (rowDelimiterCode === CRLF &&
                            data.charCodeAt(i + 1) === CH_LF) {
                            // If we see an expected \r\n, then increment to the end of the delimiter.
                            i++;
                            state = NEW_ROW;
                        }
                        else {
                            throw `string index ${i} (in row ${nrows}, column ${col}): carriage return found, but not as part of a row delimiter C ${data.charCodeAt(i + 1)}`;
                        }
                        break;
                    case CH_LF:
                        if (rowDelimiterCode === LF) {
                            state = NEW_ROW;
                        }
                        else {
                            throw `string index ${i} (in row ${nrows}, column ${col}): line feed found, but row delimiter starts with a carriage return`;
                        }
                        break;
                    default:
                        throw `string index ${i} (in row ${nrows}, column ${col}): quote in escaped field not followed by quote, delimiter, or row delimiter`;
                }
                break;
            // We are in an unquoted field, so the only thing we look for is the next
            // row or field delimiter.
            case UNQUOTED_FIELD:
                // Skip ahead to either the next field delimiter or possible start of a
                // row delimiter (CR or LF).
                while (i < endIndex) {
                    char = data.charCodeAt(i);
                    if (char === CH_DELIMITER || char === CH_LF || char === CH_CR) {
                        break;
                    }
                    i++;
                }
                // Process the character we're seeing in an unquoted field.
                switch (char) {
                    // A field delimiter means we are starting a new field.
                    case CH_DELIMITER:
                        state = NEW_FIELD;
                        break;
                    // A row delimiter means we are starting a new row in the next index.
                    case CH_CR:
                        if (rowDelimiterCode === CR) {
                            state = NEW_ROW;
                        }
                        else if (rowDelimiterCode === CRLF &&
                            data.charCodeAt(i + 1) === CH_LF) {
                            // If we see an expected \r\n, then increment to the end of the delimiter.
                            i++;
                            state = NEW_ROW;
                        }
                        else {
                            throw `string index ${i} (in row ${nrows}, column ${col}): carriage return found, but not as part of a row delimiter C ${data.charCodeAt(i + 1)}`;
                        }
                        break;
                    case CH_LF:
                        if (rowDelimiterCode === LF) {
                            state = NEW_ROW;
                        }
                        else {
                            throw `string index ${i} (in row ${nrows}, column ${col}): line feed found, but row delimiter starts with a carriage return`;
                        }
                        break;
                    // Otherwise, we continue on in the unquoted field.
                    default:
                        continue;
                }
                break;
            // We should never reach this point since the parser state is handled above,
            // so throw an error if we do.
            default:
                throw `string index ${i} (in row ${nrows}, column ${col}): state not recognized`;
        }
        // Increment i to the next character index
        i++;
        // Update return values based on state.
        switch (state) {
            case NEW_ROW:
                nrows++;
                // If ncols is undefined, set it to the number of columns in this row (first row implied).
                if (ncols === undefined) {
                    if (nrows !== 1) {
                        throw new Error('Error parsing default number of columns');
                    }
                    ncols = col;
                }
                // Pad or truncate the column offsets in the previous row if we are
                // returning them.
                if (columnOffsets === true) {
                    if (col < ncols) {
                        // We didn't have enough columns, so add some more column offsets that
                        // point to just before the row delimiter we just saw.
                        for (; col < ncols; col++) {
                            offsets.push(i - rowDelimiterLength);
                        }
                    }
                    else if (col > ncols) {
                        // We had too many columns, so truncate them.
                        offsets.length = offsets.length - (col - ncols);
                    }
                }
                // Shortcut return if nrows reaches the maximum rows we are to parse.
                if (nrows === maxRows) {
                    return { nrows, ncols: columnOffsets ? ncols : 0, offsets };
                }
                break;
            case NEW_FIELD:
                // If we are returning column offsets, log the current index.
                if (columnOffsets === true) {
                    offsets.push(i);
                }
                // Update the column counter.
                col++;
                break;
            default:
                break;
        }
    }
    // If we finished parsing and we are *not* in the NEW_ROW state, then do the
    // column padding/truncation for the last row. Also make sure ncols is
    // defined.
    if (state !== NEW_ROW) {
        nrows++;
        if (columnOffsets === true) {
            // If ncols is *still* undefined, then we only parsed one row and didn't
            // have a newline, so set it to the number of columns we found.
            if (ncols === undefined) {
                ncols = col;
            }
            if (col < ncols) {
                // We didn't have enough columns, so add some more column offsets that
                // point to just before the row delimiter we just saw.
                for (; col < ncols; col++) {
                    offsets.push(i - (rowDelimiterLength - 1));
                }
            }
            else if (col > ncols) {
                // We had too many columns, so truncate them.
                offsets.length = offsets.length - (col - ncols);
            }
        }
    }
    return { nrows, ncols: columnOffsets ? ncols !== null && ncols !== void 0 ? ncols : 0 : 0, offsets };
}
/**
 * Parse delimiter-separated data where no delimiter is quoted.
 *
 * @param options: The parser options
 * @returns An object giving the offsets for the rows or columns parsed.
 *
 * #### Notes
 * This function is an optimized parser for cases where there are no field or
 * row delimiters in quotes. Note that the data can have quotes, but they are
 * not interpreted in any special way. This implementation is based on [RFC
 * 4180](https://tools.ietf.org/html/rfc4180), but disregards quotes.
 */
function parseDSVNoQuotes(options) {
    // Set option defaults.
    const { data, columnOffsets, delimiter = ',', rowDelimiter = '\r\n', startIndex = 0, maxRows = 0xffffffff } = options;
    // ncols will be set automatically if it is undefined.
    let ncols = options.ncols;
    // Set up our return variables.
    const offsets = [];
    let nrows = 0;
    // Set up various state variables.
    const rowDelimiterLength = rowDelimiter.length;
    let currRow = startIndex;
    const len = data.length;
    let nextRow;
    let col;
    let rowString;
    let colIndex;
    // The end of the current row.
    let rowEnd;
    // Start parsing at the start index.
    nextRow = startIndex;
    // Loop through rows until we run out of data or we've reached maxRows.
    while (nextRow !== -1 && nrows < maxRows && currRow < len) {
        // Store the offset for the beginning of the row and increment the rows.
        offsets.push(currRow);
        nrows++;
        // Find the next row delimiter.
        nextRow = data.indexOf(rowDelimiter, currRow);
        // If the next row delimiter is not found, set the end of the row to the
        // end of the data string.
        rowEnd = nextRow === -1 ? len : nextRow;
        // If we are returning column offsets, push them onto the array.
        if (columnOffsets === true) {
            // Find the next field delimiter. We slice the current row out so that
            // the indexOf will stop at the end of the row. It may possibly be faster
            // to just use a loop to check each character.
            col = 1;
            rowString = data.slice(currRow, rowEnd);
            colIndex = rowString.indexOf(delimiter);
            if (ncols === undefined) {
                // If we don't know how many columns we need, loop through and find all
                // of the field delimiters in this row.
                while (colIndex !== -1) {
                    offsets.push(currRow + colIndex + 1);
                    col++;
                    colIndex = rowString.indexOf(delimiter, colIndex + 1);
                }
                // Set ncols to the number of fields we found.
                ncols = col;
            }
            else {
                // If we know the number of columns we expect, find the field delimiters
                // up to that many columns.
                while (colIndex !== -1 && col < ncols) {
                    offsets.push(currRow + colIndex + 1);
                    col++;
                    colIndex = rowString.indexOf(delimiter, colIndex + 1);
                }
                // If we didn't reach the number of columns we expected, pad the offsets
                // with the offset just before the row delimiter.
                while (col < ncols) {
                    offsets.push(rowEnd);
                    col++;
                }
            }
        }
        // Skip past the row delimiter at the end of the row.
        currRow = rowEnd + rowDelimiterLength;
    }
    return { nrows, ncols: columnOffsets ? ncols !== null && ncols !== void 0 ? ncols : 0 : 0, offsets };
}


/***/ }),

/***/ "../packages/csvviewer/lib/toolbar.js":
/*!********************************************!*\
  !*** ../packages/csvviewer/lib/toolbar.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CSVDelimiter": () => (/* binding */ CSVDelimiter)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The class name added to a csv toolbar widget.
 */
const CSV_DELIMITER_CLASS = 'jp-CSVDelimiter';
const CSV_DELIMITER_LABEL_CLASS = 'jp-CSVDelimiter-label';
/**
 * The class name added to a csv toolbar's dropdown element.
 */
const CSV_DELIMITER_DROPDOWN_CLASS = 'jp-CSVDelimiter-dropdown';
/**
 * A widget for selecting a delimiter.
 */
class CSVDelimiter extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    /**
     * Construct a new csv table widget.
     */
    constructor(options) {
        super({ node: Private.createNode(options.selected, options.translator) });
        this._delimiterChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this.addClass(CSV_DELIMITER_CLASS);
    }
    /**
     * A signal emitted when the delimiter selection has changed.
     */
    get delimiterChanged() {
        return this._delimiterChanged;
    }
    /**
     * The delimiter dropdown menu.
     */
    get selectNode() {
        return this.node.getElementsByTagName('select')[0];
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'change':
                this._delimiterChanged.emit(this.selectNode.value);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        this.selectNode.addEventListener('change', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        this.selectNode.removeEventListener('change', this);
    }
}
/**
 * A namespace for private toolbar methods.
 */
var Private;
(function (Private) {
    /**
     * Create the node for the delimiter switcher.
     */
    function createNode(selected, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        const trans = translator === null || translator === void 0 ? void 0 : translator.load('jupyterlab');
        // The supported parsing delimiters and labels.
        const delimiters = [
            [',', ','],
            [';', ';'],
            ['\t', trans.__('tab')],
            ['|', trans.__('pipe')],
            ['#', trans.__('hash')]
        ];
        const div = document.createElement('div');
        const label = document.createElement('span');
        const select = document.createElement('select');
        label.textContent = trans.__('Delimiter: ');
        label.className = CSV_DELIMITER_LABEL_CLASS;
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.each)(delimiters, ([delimiter, label]) => {
            const option = document.createElement('option');
            option.value = delimiter;
            option.textContent = label;
            if (delimiter === selected) {
                option.selected = true;
            }
            select.appendChild(option);
        });
        div.appendChild(label);
        const node = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Styling.wrapSelect(select);
        node.classList.add(CSV_DELIMITER_DROPDOWN_CLASS);
        div.appendChild(node);
        return div;
    }
    Private.createNode = createNode;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/csvviewer/lib/widget.js":
/*!*******************************************!*\
  !*** ../packages/csvviewer/lib/widget.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TextRenderConfig": () => (/* binding */ TextRenderConfig),
/* harmony export */   "GridSearchService": () => (/* binding */ GridSearchService),
/* harmony export */   "CSVViewer": () => (/* binding */ CSVViewer),
/* harmony export */   "CSVDocumentWidget": () => (/* binding */ CSVDocumentWidget),
/* harmony export */   "CSVViewerFactory": () => (/* binding */ CSVViewerFactory),
/* harmony export */   "TSVViewerFactory": () => (/* binding */ TSVViewerFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/datagrid */ "webpack/sharing/consume/default/@lumino/datagrid/@lumino/datagrid");
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_datagrid__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./model */ "../packages/csvviewer/lib/model.js");
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./toolbar */ "../packages/csvviewer/lib/toolbar.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __rest = (undefined && undefined.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};








/**
 * The class name added to a CSV viewer.
 */
const CSV_CLASS = 'jp-CSVViewer';
/**
 * The class name added to a CSV viewer datagrid.
 */
const CSV_GRID_CLASS = 'jp-CSVViewer-grid';
/**
 * The timeout to wait for change activity to have ceased before rendering.
 */
const RENDER_TIMEOUT = 1000;
/**
 * Configuration for cells textrenderer.
 */
class TextRenderConfig {
}
/**
 * Search service remembers the search state and the location of the last
 * match, for incremental searching.
 * Search service is also responsible of providing a cell renderer function
 * to set the background color of cells matching the search text.
 */
class GridSearchService {
    constructor(grid) {
        this._looping = true;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._grid = grid;
        this._query = null;
        this._row = 0;
        this._column = -1;
    }
    /**
     * A signal fired when the grid changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Returns a cellrenderer config function to render each cell background.
     * If cell match, background is matchBackgroundColor, if it's the current
     * match, background is currentMatchBackgroundColor.
     */
    cellBackgroundColorRendererFunc(config) {
        return ({ value, row, column }) => {
            if (this._query) {
                if (value.match(this._query)) {
                    if (this._row === row && this._column === column) {
                        return config.currentMatchBackgroundColor;
                    }
                    return config.matchBackgroundColor;
                }
            }
            return '';
        };
    }
    /**
     * Clear the search.
     */
    clear() {
        this._query = null;
        this._row = 0;
        this._column = -1;
        this._changed.emit(undefined);
    }
    /**
     * incrementally look for searchText.
     */
    find(query, reverse = false) {
        const model = this._grid.dataModel;
        const rowCount = model.rowCount('body');
        const columnCount = model.columnCount('body');
        if (this._query !== query) {
            // reset search
            this._row = 0;
            this._column = -1;
        }
        this._query = query;
        // check if the match is in current viewport
        const minRow = this._grid.scrollY / this._grid.defaultSizes.rowHeight;
        const maxRow = (this._grid.scrollY + this._grid.pageHeight) /
            this._grid.defaultSizes.rowHeight;
        const minColumn = this._grid.scrollX / this._grid.defaultSizes.columnHeaderHeight;
        const maxColumn = (this._grid.scrollX + this._grid.pageWidth) /
            this._grid.defaultSizes.columnHeaderHeight;
        const isInViewport = (row, column) => {
            return (row >= minRow &&
                row <= maxRow &&
                column >= minColumn &&
                column <= maxColumn);
        };
        const increment = reverse ? -1 : 1;
        this._column += increment;
        for (let row = this._row; reverse ? row >= 0 : row < rowCount; row += increment) {
            for (let col = this._column; reverse ? col >= 0 : col < columnCount; col += increment) {
                const cellData = model.data('body', row, col);
                if (cellData.match(query)) {
                    // to update the background of matching cells.
                    // TODO: we only really need to invalidate the previous and current
                    // cell rects, not the entire grid.
                    this._changed.emit(undefined);
                    if (!isInViewport(row, col)) {
                        this._grid.scrollToRow(row);
                    }
                    this._row = row;
                    this._column = col;
                    return true;
                }
            }
            this._column = reverse ? columnCount - 1 : 0;
        }
        // We've finished searching all the way to the limits of the grid. If this
        // is the first time through (looping is true), wrap the indices and search
        // again. Otherwise, give up.
        if (this._looping) {
            this._looping = false;
            this._row = reverse ? 0 : rowCount - 1;
            this._wrapRows(reverse);
            try {
                return this.find(query, reverse);
            }
            finally {
                this._looping = true;
            }
        }
        return false;
    }
    /**
     * Wrap indices if needed to just before the start or just after the end.
     */
    _wrapRows(reverse = false) {
        const model = this._grid.dataModel;
        const rowCount = model.rowCount('body');
        const columnCount = model.columnCount('body');
        if (reverse && this._row <= 0) {
            // if we are at the front, wrap to just past the end.
            this._row = rowCount - 1;
            this._column = columnCount;
        }
        else if (!reverse && this._row >= rowCount - 1) {
            // if we are at the end, wrap to just before the front.
            this._row = 0;
            this._column = -1;
        }
    }
    get query() {
        return this._query;
    }
}
/**
 * A viewer for CSV tables.
 */
class CSVViewer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget {
    /**
     * Construct a new CSV viewer.
     */
    constructor(options) {
        super();
        this._monitor = null;
        this._delimiter = ',';
        this._revealed = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
        this._baseRenderer = null;
        const context = (this._context = options.context);
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.PanelLayout());
        this.addClass(CSV_CLASS);
        this._grid = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_3__.DataGrid({
            defaultSizes: {
                rowHeight: 24,
                columnWidth: 144,
                rowHeaderWidth: 64,
                columnHeaderHeight: 36
            }
        });
        this._grid.addClass(CSV_GRID_CLASS);
        this._grid.headerVisibility = 'all';
        this._grid.keyHandler = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_3__.BasicKeyHandler();
        this._grid.mouseHandler = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_3__.BasicMouseHandler();
        this._grid.copyConfig = {
            separator: '\t',
            format: _lumino_datagrid__WEBPACK_IMPORTED_MODULE_3__.DataGrid.copyFormatGeneric,
            headers: 'all',
            warningThreshold: 1e6
        };
        layout.addWidget(this._grid);
        this._searchService = new GridSearchService(this._grid);
        this._searchService.changed.connect(this._updateRenderer, this);
        void this._context.ready.then(() => {
            this._updateGrid();
            this._revealed.resolve(undefined);
            // Throttle the rendering rate of the widget.
            this._monitor = new _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.ActivityMonitor({
                signal: context.model.contentChanged,
                timeout: RENDER_TIMEOUT
            });
            this._monitor.activityStopped.connect(this._updateGrid, this);
        });
    }
    /**
     * The CSV widget's context.
     */
    get context() {
        return this._context;
    }
    /**
     * A promise that resolves when the csv viewer is ready to be revealed.
     */
    get revealed() {
        return this._revealed.promise;
    }
    /**
     * The delimiter for the file.
     */
    get delimiter() {
        return this._delimiter;
    }
    set delimiter(value) {
        if (value === this._delimiter) {
            return;
        }
        this._delimiter = value;
        this._updateGrid();
    }
    /**
     * The style used by the data grid.
     */
    get style() {
        return this._grid.style;
    }
    set style(value) {
        this._grid.style = value;
    }
    /**
     * The config used to create text renderer.
     */
    set rendererConfig(rendererConfig) {
        this._baseRenderer = rendererConfig;
        this._updateRenderer();
    }
    /**
     * The search service
     */
    get searchService() {
        return this._searchService;
    }
    /**
     * Dispose of the resources used by the widget.
     */
    dispose() {
        if (this._monitor) {
            this._monitor.dispose();
        }
        super.dispose();
    }
    /**
     * Go to line
     */
    goToLine(lineNumber) {
        this._grid.scrollToRow(lineNumber);
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.tabIndex = -1;
        this.node.focus();
    }
    /**
     * Create the model for the grid.
     */
    _updateGrid() {
        const data = this._context.model.toString();
        const delimiter = this._delimiter;
        const oldModel = this._grid.dataModel;
        const dataModel = (this._grid.dataModel = new _model__WEBPACK_IMPORTED_MODULE_6__.DSVModel({
            data,
            delimiter
        }));
        this._grid.selectionModel = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_3__.BasicSelectionModel({ dataModel });
        if (oldModel) {
            oldModel.dispose();
        }
    }
    /**
     * Update the renderer for the grid.
     */
    _updateRenderer() {
        if (this._baseRenderer === null) {
            return;
        }
        const rendererConfig = this._baseRenderer;
        const renderer = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_3__.TextRenderer({
            textColor: rendererConfig.textColor,
            horizontalAlignment: rendererConfig.horizontalAlignment,
            backgroundColor: this._searchService.cellBackgroundColorRendererFunc(rendererConfig)
        });
        this._grid.cellRenderers.update({
            body: renderer,
            'column-header': renderer,
            'corner-header': renderer,
            'row-header': renderer
        });
    }
}
/**
 * A document widget for CSV content widgets.
 */
class CSVDocumentWidget extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget {
    constructor(options) {
        let { content, context, delimiter, reveal } = options, other = __rest(options, ["content", "context", "delimiter", "reveal"]);
        content = content || Private.createContent(context);
        reveal = Promise.all([reveal, content.revealed]);
        super(Object.assign({ content, context, reveal }, other));
        if (delimiter) {
            content.delimiter = delimiter;
        }
        const csvDelimiter = new _toolbar__WEBPACK_IMPORTED_MODULE_7__.CSVDelimiter({ selected: content.delimiter });
        this.toolbar.addItem('delimiter', csvDelimiter);
        csvDelimiter.delimiterChanged.connect((sender, delimiter) => {
            content.delimiter = delimiter;
        });
    }
    /**
     * Set URI fragment identifier for rows
     */
    setFragment(fragment) {
        const parseFragments = fragment.split('=');
        // TODO: expand to allow columns and cells to be selected
        // reference: https://tools.ietf.org/html/rfc7111#section-3
        if (parseFragments[0] !== '#row') {
            return;
        }
        // multiple rows, separated by semi-colons can be provided, we will just
        // go to the top one
        let topRow = parseFragments[1].split(';')[0];
        // a range of rows can be provided, we will take the first value
        topRow = topRow.split('-')[0];
        // go to that row
        void this.context.ready.then(() => {
            this.content.goToLine(Number(topRow));
        });
    }
}
var Private;
(function (Private) {
    function createContent(context) {
        return new CSVViewer({ context });
    }
    Private.createContent = createContent;
})(Private || (Private = {}));
/**
 * A widget factory for CSV widgets.
 */
class CSVViewerFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const translator = this.translator;
        return new CSVDocumentWidget({ context, translator });
    }
}
/**
 * A widget factory for TSV widgets.
 */
class TSVViewerFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const delimiter = '\t';
        return new CSVDocumentWidget({
            context,
            delimiter,
            translator: this.translator
        });
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY3N2dmlld2VyL3NyYy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY3N2dmlld2VyL3NyYy9tb2RlbC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY3N2dmlld2VyL3NyYy9wYXJzZS50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY3N2dmlld2VyL3NyYy90b29sYmFyLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jc3Z2aWV3ZXIvc3JjL3dpZGdldC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBRXFCO0FBQ0E7QUFDRTtBQUNEOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNWekIsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUVQO0FBQ1A7QUFFaUI7QUFFOUQ7Ozs7Ozs7Ozs7O0VBV0U7QUFFRjs7R0FFRztBQUNILE1BQU0sT0FBTyxHQUErQjtJQUMxQyxNQUFNLEVBQUUsNENBQVE7SUFDaEIsUUFBUSxFQUFFLG9EQUFnQjtDQUMzQixDQUFDO0FBRUY7Ozs7O0dBS0c7QUFDSSxNQUFNLFFBQVMsU0FBUSx1REFBUztJQUNyQzs7OztPQUlHO0lBQ0gsWUFBWSxPQUEwQjtRQUNwQyxLQUFLLEVBQUUsQ0FBQztRQWtsQkYsY0FBUyxHQUF1QixDQUFDLENBQUM7UUFHMUMsb0JBQW9CO1FBQ3BCOztXQUVHO1FBQ0ssWUFBTyxHQUFhLEVBQUUsQ0FBQztRQUMvQjs7Ozs7O1dBTUc7UUFDSyxtQkFBYyxHQUFnQixJQUFJLFdBQVcsQ0FBQyxD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UyxHQUFHLElBQUksQ0FBQztRQUN2QixPQUFPLElBQUksaUJBQWlCLENBQUM7WUFDM0IsT0FBTztZQUNQLFNBQVM7WUFDVCxVQUFVLEVBQUUsSUFBSSxDQUFDLFVBQVU7U0FDNUIsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztDQUNGIiwiZmlsZSI6InBhY2thZ2VzX2NzdnZpZXdlcl9saWJfaW5kZXhfanMuY2JjZTViNjY4NDg4NmU0YTQxMTAuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBjc3Z2aWV3ZXJcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL21vZGVsJztcbmV4cG9ydCAqIGZyb20gJy4vcGFyc2UnO1xuZXhwb3J0ICogZnJvbSAnLi90b29sYmFyJztcbmV4cG9ydCAqIGZyb20gJy4vd2lkZ2V0JztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgUHJvbWlzZURlbGVnYXRlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgRGF0YU1vZGVsIH0gZnJvbSAnQGx1bWluby9kYXRhZ3JpZCc7XG5pbXBvcnQgeyBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBJUGFyc2VyLCBwYXJzZURTViwgcGFyc2VEU1ZOb1F1b3RlcyB9IGZyb20gJy4vcGFyc2UnO1xuXG4vKlxuUG9zc2libGUgaWRlYXMgZm9yIGZ1cnRoZXIgaW1wbGVtZW50YXRpb246XG5cbi0gU2hvdyBhIHNwaW5uZXIgb3Igc29tZXRoaW5nIHZpc2libGUgd2hlbiB3ZSBhcmUgZG9pbmcgZGVsYXllZCBwYXJzaW5nLlxuLSBUaGUgY2FjaGUgcmlnaHQgbm93IGhhbmRsZXMgc2Nyb2xsaW5nIGRvd24gZ3JlYXQgLSBpdCBnZXRzIHRoZSBuZXh0IHNldmVyYWwgaHVuZHJlZCByb3dzLiBIb3dldmVyLCBzY3JvbGxpbmcgdXAgY2F1c2VzIGxvdHMgb2YgY2FjaGUgbWlzc2VzIC0gZWFjaCBuZXcgcm93IGNhdXNlcyBhIGZsdXNoIG9mIHRoZSBjYWNoZS4gV2hlbiBpbnZhbGlkYXRpbmcgYW4gZW50aXJlIGNhY2hlLCB3ZSBzaG91bGQgcHV0IHRoZSByZXF1ZXN0ZWQgcm93IGluIG1pZGRsZSBvZiB0aGUgY2FjaGUgKGFkanVzdGluZyBmb3Igcm93cyBhdCB0aGUgYmVnaW5uaW5nIG9yIGVuZCkuIFdoZW4gcG9wdWxhdGluZyBhIGNhY2hlLCB3ZSBzaG91bGQgcmV0cmlldmUgcm93cyBib3RoIGFib3ZlIGFuZCBiZWxvdyB0aGUgcmVxdWVzdGVkIHJvdy5cbi0gV2hlbiB3ZSBoYXZlIGEgaGVhZGVyLCBhbmQgd2UgYXJlIGd1ZXNzaW5nIHRoZSBwYXJzZXIgdG8gdXNlLCB0cnkgY2hlY2tpbmcganVzdCB0aGUgcGFydCBvZiB0aGUgZmlsZSAqYWZ0ZXIqIHRoZSBoZWFkZXIgcm93IGZvciBxdW90ZXMuIEkgdGhpbmsgb2Z0ZW4gYSBmaXJzdCBoZWFkZXIgcm93IGlzIHF1b3RlZCwgYnV0IHRoZSByZXN0IG9mIHRoZSBmaWxlIGlzIG5vdCBhbmQgY2FuIGJlIHBhcnNlZCBtdWNoIGZhc3Rlci5cbi0gYXV0ZGV0ZWN0IHRoZSBkZWxpbWl0ZXIgKGxvb2sgZm9yIGNvbW1hLCB0YWIsIHNlbWljb2xvbiBpbiBmaXJzdCBsaW5lLiBJZiBtb3JlIHRoYW4gb25lIGZvdW5kLCBwYXJzZSBmaXJzdCByb3cgd2l0aCBjb21tYSwgdGFiLCBzZW1pY29sb24gZGVsaW1pdGVycy4gT25lIHdpdGggbW9zdCBmaWVsZHMgd2lucykuXG4tIFRvb2xiYXIgYnV0dG9ucyB0byBjb250cm9sIHRoZSByb3cgZGVsaW1pdGVyLCB0aGUgcGFyc2luZyBlbmdpbmUgKHF1b3RlZC9ub3QgcXVvdGVkKSwgdGhlIHF1b3RlIGNoYXJhY3RlciwgZXRjLlxuLSBJbnZlc3RpZ2F0ZSBpbmNyZW1lbnRhbCBsb2FkaW5nIHN0cmF0ZWdpZXMgaW4gdGhlIHBhcnNlQXN5bmMgZnVuY3Rpb24uIEluIGluaXRpYWwgaW52ZXN0aWdhdGlvbnMsIHNldHRpbmcgdGhlIGNodW5rIHNpemUgdG8gMTAwayBpbiBwYXJzZUFzeW5jIHNlZW1zIGNhdXNlIGluc3RhYmlsaXR5IHdpdGggbGFyZ2UgZmlsZXMgaW4gQ2hyb21lIChzdWNoIGFzIDgtbWlsbGlvbiByb3cgZmlsZXMpLiBQZXJoYXBzIHRoaXMgaXMgYmVjYXVzZSB3ZSBhcmUgcmVjeWNsaW5nIHRoZSByb3cgb2Zmc2V0IGFuZCBjb2x1bW4gb2Zmc2V0IGFycmF5cyBxdWlja2x5PyBJdCBkb2Vzbid0IHNlZW0gdGhhdCB0aGVyZSBpcyBhIG1lbW9yeSBsZWFrLiBPbiB0aGlzIHRoZW9yeSwgcGVyaGFwcyB3ZSBqdXN0IG5lZWQgdG8ga2VlcCB0aGUgb2Zmc2V0cyBsaXN0IGFuIGFjdHVhbCBsaXN0LCBhbmQgcGFzcyBpdCBpbnRvIHRoZSBwYXJzaW5nIGZ1bmN0aW9uIHRvIGV4dGVuZCB3aXRob3V0IGNvcHlpbmcsIGFuZCBmaW5hbGl6ZSBpdCBpbnRvIGFuIGFycmF5IGJ1ZmZlciBvbmx5IHdoZW4gd2UgYXJlIGRvbmUgcGFyc2luZy4gT3IgcGVyaGFwcyB3ZSBkb3VibGUgdGhlIHNpemUgb2YgdGhlIGFycmF5IGJ1ZmZlciBlYWNoIHRpbWUsIHdoaWNoIG1heSBiZSB3YXN0ZWZ1bCwgYnV0IGF0IHRoZSBlbmQgd2UgdHJpbSBpdCBkb3duIGlmIGl0J3MgdG9vIHdhc3RlZnVsIChwZXJoYXBzIHdlIGhhdmUgb3VyIG93biBvYmplY3QgdGhhdCBpcyBiYWNrZWQgYnkgYW4gYXJyYXkgYnVmZmVyLCBidXQgaGFzIGEgcHVzaCBtZXRob2QgdGhhdCB3aWxsIGF1dG9tYXRpY2FsbHkgZG91YmxlIHRoZSBhcnJheSBidWZmZXIgc2l6ZSBhcyBuZWVkZWQsIGFuZCBhIHRyaW0gZnVuY3Rpb24gdG8gZmluYWxpemUgdGhlIGFycmF5IHRvIGV4YWN0bHkgdGhlIHNpemUgbmVlZGVkKT8gT3IgcGVyaGFwcyB3ZSBkb24ndCB1c2UgYXJyYXkgYnVmZmVycyBhdCBhbGwgLSBjb21wYXJlIHRoZSBtZW1vcnkgY29zdCBhbmQgc3BlZWQgb2Yga2VlcGluZyB0aGUgb2Zmc2V0cyBhcyBsaXN0cyBpbnN0ZWFkIG9mIG1lbW9yeSBidWZmZXJzLlxuLSBJbnZlc3RpZ2F0ZSBhIHRpbWUtYmFzZWQgaW5jcmVtZW50YWwgcGFyc2luZyBzdHJhdGVneSwgcmF0aGVyIHRoYW4gYSByb3ctYmFzZWQgb25lLiBUaGUgcGFyc2VyIGNvdWxkIHRha2UgYSBtYXhpbXVtIHRpbWUgdG8gcGFyc2UgKHNheSAzMDBtcyksIGFuZCB3aWxsIHBhcnNlIHVwIHRvIHRoYXQgZHVyYXRpb24sIGluIHdoaWNoIGNhc2UgdGhlIHBhcnNlciBwcm9iYWJseSBhbHNvIG5lZWRzIGEgd2F5IHRvIG5vdGlmeSB3aGVuIGl0IGhhcyByZWFjaGVkIHRoZSBlbmQgb2YgYSBmaWxlLlxuLSBGb3IgdmVyeSBsYXJnZSBmaWxlcywgd2hlcmUgd2UgYXJlIG9ubHkgc3RvcmluZyBhIHNtYWxsIGNhY2hlLCBzY3JvbGxpbmcgaXMgdmVyeSBsYWdneSBpbiBTYWZhcmkuIEl0IHdvdWxkIGJlIGdvb2QgdG8gcHJvZmlsZSBpdC5cbiovXG5cbi8qKlxuICogUG9zc2libGUgZGVsaW1pdGVyLXNlcGFyYXRlZCBkYXRhIHBhcnNlcnMuXG4gKi9cbmNvbnN0IFBBUlNFUlM6IHsgW2tleTogc3RyaW5nXTogSVBhcnNlciB9ID0ge1xuICBxdW90ZXM6IHBhcnNlRFNWLFxuICBub3F1b3RlczogcGFyc2VEU1ZOb1F1b3Rlc1xufTtcblxuLyoqXG4gKiBBIGRhdGEgbW9kZWwgaW1wbGVtZW50YXRpb24gZm9yIGluLW1lbW9yeSBkZWxpbWl0ZXItc2VwYXJhdGVkIGRhdGEuXG4gKlxuICogIyMjIyBOb3Rlc1xuICogVGhpcyBtb2RlbCBoYW5kbGVzIGRhdGEgd2l0aCB1cCB0byAyKiozMiBjaGFyYWN0ZXJzLlxuICovXG5leHBvcnQgY2xhc3MgRFNWTW9kZWwgZXh0ZW5kcyBEYXRhTW9kZWwgaW1wbGVtZW50cyBJRGlzcG9zYWJsZSB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBkYXRhIG1vZGVsIHdpdGggc3RhdGljIENTViBkYXRhLlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBvcHRpb25zIGZvciBpbml0aWFsaXppbmcgdGhlIGRhdGEgbW9kZWwuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBEU1ZNb2RlbC5JT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgbGV0IHtcbiAgICAgIGRhdGEsXG4gICAgICBkZWxpbWl0ZXIgPSAnLCcsXG4gICAgICByb3dEZWxpbWl0ZXIgPSB1bmRlZmluZWQsXG4gICAgICBxdW90ZSA9ICdcIicsXG4gICAgICBxdW90ZVBhcnNlciA9IHVuZGVmaW5lZCxcbiAgICAgIGhlYWRlciA9IHRydWUsXG4gICAgICBpbml0aWFsUm93cyA9IDUwMFxuICAgIH0gPSBvcHRpb25zO1xuICAgIHRoaXMuX3Jhd0RhdGEgPSBkYXRhO1xuICAgIHRoaXMuX2RlbGltaXRlciA9IGRlbGltaXRlcjtcbiAgICB0aGlzLl9xdW90ZSA9IHF1b3RlO1xuICAgIHRoaXMuX3F1b3RlRXNjYXBlZCA9IG5ldyBSZWdFeHAocXVvdGUgKyBxdW90ZSwgJ2cnKTtcbiAgICB0aGlzLl9pbml0aWFsUm93cyA9IGluaXRpYWxSb3dzO1xuXG4gICAgLy8gR3Vlc3MgdGhlIHJvdyBkZWxpbWl0ZXIgaWYgaXQgd2FzIG5vdCBzdXBwbGllZC4gVGhpcyB3aWxsIGJlIGZvb2xlZCBpZiBhXG4gICAgLy8gZGlmZmVyZW50IGxpbmUgZGVsaW1pdGVyIHBvc3NpYmlsaXR5IGFwcGVhcnMgaW4gdGhlIGZpcnN0IHJvdy5cbiAgICBpZiAocm93RGVsaW1pdGVyID09PSB1bmRlZmluZWQpIHtcbiAgICAgIGNvbnN0IGkgPSBkYXRhLnNsaWNlKDAsIDUwMDApLmluZGV4T2YoJ1xccicpO1xuICAgICAgaWYgKGkgPT09IC0xKSB7XG4gICAgICAgIHJvd0RlbGltaXRlciA9ICdcXG4nO1xuICAgICAgfSBlbHNlIGlmIChkYXRhW2kgKyAxXSA9PT0gJ1xcbicpIHtcbiAgICAgICAgcm93RGVsaW1pdGVyID0gJ1xcclxcbic7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICByb3dEZWxpbWl0ZXIgPSAnXFxyJztcbiAgICAgIH1cbiAgICB9XG4gICAgdGhpcy5fcm93RGVsaW1pdGVyID0gcm93RGVsaW1pdGVyO1xuXG4gICAgaWYgKHF1b3RlUGFyc2VyID09PSB1bmRlZmluZWQpIHtcbiAgICAgIC8vIENoZWNrIGZvciB0aGUgZXhpc3RlbmNlIG9mIHF1b3RlcyBpZiB0aGUgcXVvdGVQYXJzZXIgaXMgbm90IHNldC5cbiAgICAgIHF1b3RlUGFyc2VyID0gZGF0YS5pbmRleE9mKHF1b3RlKSA+PSAwO1xuICAgIH1cbiAgICB0aGlzLl9wYXJzZXIgPSBxdW90ZVBhcnNlciA/ICdxdW90ZXMnIDogJ25vcXVvdGVzJztcblxuICAgIC8vIFBhcnNlIHRoZSBkYXRhLlxuICAgIHRoaXMucGFyc2VBc3luYygpO1xuXG4gICAgLy8gQ2FjaGUgdGhlIGhlYWRlciByb3cuXG4gICAgaWYgKGhlYWRlciA9PT0gdHJ1ZSAmJiB0aGlzLl9jb2x1bW5Db3VudCEgPiAwKSB7XG4gICAgICBjb25zdCBoID0gW107XG4gICAgICBmb3IgKGxldCBjID0gMDsgYyA8IHRoaXMuX2NvbHVtbkNvdW50ITsgYysrKSB7XG4gICAgICAgIGgucHVzaCh0aGlzLl9nZXRGaWVsZCgwLCBjKSk7XG4gICAgICB9XG4gICAgICB0aGlzLl9oZWFkZXIgPSBoO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoaXMgbW9kZWwgaGFzIGJlZW4gZGlzcG9zZWQuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBtb2RlbCBoYXMgcGFyc2VkIGFsbCBvZiBpdHMgZGF0YS5cbiAgICovXG4gIGdldCByZWFkeSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5fcmVhZHkucHJvbWlzZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgc3RyaW5nIHJlcHJlc2VudGF0aW9uIG9mIHRoZSBkYXRhLlxuICAgKi9cbiAgZ2V0IHJhd0RhdGEoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5fcmF3RGF0YTtcbiAgfVxuICBzZXQgcmF3RGF0YSh2YWx1ZTogc3RyaW5nKSB7XG4gICAgdGhpcy5fcmF3RGF0YSA9IHZhbHVlO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBpbml0aWFsIGNodW5rIG9mIHJvd3MgdG8gcGFyc2UuXG4gICAqL1xuICBnZXQgaW5pdGlhbFJvd3MoKTogbnVtYmVyIHtcbiAgICByZXR1cm4gdGhpcy5faW5pdGlhbFJvd3M7XG4gIH1cbiAgc2V0IGluaXRpYWxSb3dzKHZhbHVlOiBudW1iZXIpIHtcbiAgICB0aGlzLl9pbml0aWFsUm93cyA9IHZhbHVlO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBoZWFkZXIgc3RyaW5ncy5cbiAgICovXG4gIGdldCBoZWFkZXIoKTogc3RyaW5nW10ge1xuICAgIHJldHVybiB0aGlzLl9oZWFkZXI7XG4gIH1cbiAgc2V0IGhlYWRlcih2YWx1ZTogc3RyaW5nW10pIHtcbiAgICB0aGlzLl9oZWFkZXIgPSB2YWx1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVsaW1pdGVyIGJldHdlZW4gZW50cmllcyBvbiB0aGUgc2FtZSByb3cuXG4gICAqL1xuICBnZXQgZGVsaW1pdGVyKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX2RlbGltaXRlcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVsaW1pdGVyIGJldHdlZW4gcm93cy5cbiAgICovXG4gIGdldCByb3dEZWxpbWl0ZXIoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5fcm93RGVsaW1pdGVyO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgYm9vbGVhbiBkZXRlcm1pbmVkIGJ5IHdoZXRoZXIgcGFyc2luZyBoYXMgY29tcGxldGVkLlxuICAgKi9cbiAgZ2V0IGRvbmVQYXJzaW5nKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9kb25lUGFyc2luZztcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHJvdyBjb3VudCBmb3IgYSByZWdpb24gaW4gdGhlIGRhdGEgbW9kZWwuXG4gICAqXG4gICAqIEBwYXJhbSByZWdpb24gLSBUaGUgcm93IHJlZ2lvbiBvZiBpbnRlcmVzdC5cbiAgICpcbiAgICogQHJldHVybnMgLSBUaGUgcm93IGNvdW50IGZvciB0aGUgcmVnaW9uLlxuICAgKi9cbiAgcm93Q291bnQocmVnaW9uOiBEYXRhTW9kZWwuUm93UmVnaW9uKTogbnVtYmVyIHtcbiAgICBpZiAocmVnaW9uID09PSAnYm9keScpIHtcbiAgICAgIGlmICh0aGlzLl9oZWFkZXIubGVuZ3RoID09PSAwKSB7XG4gICAgICAgIHJldHVybiB0aGlzLl9yb3dDb3VudCE7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICByZXR1cm4gdGhpcy5fcm93Q291bnQhIC0gMTtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIDE7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBjb2x1bW4gY291bnQgZm9yIGEgcmVnaW9uIGluIHRoZSBkYXRhIG1vZGVsLlxuICAgKlxuICAgKiBAcGFyYW0gcmVnaW9uIC0gVGhlIGNvbHVtbiByZWdpb24gb2YgaW50ZXJlc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIC0gVGhlIGNvbHVtbiBjb3VudCBmb3IgdGhlIHJlZ2lvbi5cbiAgICovXG4gIGNvbHVtbkNvdW50KHJlZ2lvbjogRGF0YU1vZGVsLkNvbHVtblJlZ2lvbik6IG51bWJlciB7XG4gICAgaWYgKHJlZ2lvbiA9PT0gJ2JvZHknKSB7XG4gICAgICByZXR1cm4gdGhpcy5fY29sdW1uQ291bnQhO1xuICAgIH1cbiAgICByZXR1cm4gMTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGRhdGEgdmFsdWUgZm9yIGEgY2VsbCBpbiB0aGUgZGF0YSBtb2RlbC5cbiAgICpcbiAgICogQHBhcmFtIHJlZ2lvbiAtIFRoZSBjZWxsIHJlZ2lvbiBvZiBpbnRlcmVzdC5cbiAgICpcbiAgICogQHBhcmFtIHJvdyAtIFRoZSByb3cgaW5kZXggb2YgdGhlIGNlbGwgb2YgaW50ZXJlc3QuXG4gICAqXG4gICAqIEBwYXJhbSBjb2x1bW4gLSBUaGUgY29sdW1uIGluZGV4IG9mIHRoZSBjZWxsIG9mIGludGVyZXN0LlxuICAgKlxuICAgKiBAcGFyYW0gcmV0dXJucyAtIFRoZSBkYXRhIHZhbHVlIGZvciB0aGUgc3BlY2lmaWVkIGNlbGwuXG4gICAqL1xuICBkYXRhKHJlZ2lvbjogRGF0YU1vZGVsLkNlbGxSZWdpb24sIHJvdzogbnVtYmVyLCBjb2x1bW46IG51bWJlcik6IHN0cmluZyB7XG4gICAgbGV0IHZhbHVlOiBzdHJpbmc7XG5cbiAgICAvLyBMb29rIHVwIHRoZSBmaWVsZCBhbmQgdmFsdWUgZm9yIHRoZSByZWdpb24uXG4gICAgc3dpdGNoIChyZWdpb24pIHtcbiAgICAgIGNhc2UgJ2JvZHknOlxuICAgICAgICBpZiAodGhpcy5faGVhZGVyLmxlbmd0aCA9PT0gMCkge1xuICAgICAgICAgIHZhbHVlID0gdGhpcy5fZ2V0RmllbGQocm93LCBjb2x1bW4pO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIHZhbHVlID0gdGhpcy5fZ2V0RmllbGQocm93ICsgMSwgY29sdW1uKTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2NvbHVtbi1oZWFkZXInOlxuICAgICAgICBpZiAodGhpcy5faGVhZGVyLmxlbmd0aCA9PT0gMCkge1xuICAgICAgICAgIHZhbHVlID0gKGNvbHVtbiArIDEpLnRvU3RyaW5nKCk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgdmFsdWUgPSB0aGlzLl9oZWFkZXJbY29sdW1uXTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3Jvdy1oZWFkZXInOlxuICAgICAgICB2YWx1ZSA9IChyb3cgKyAxKS50b1N0cmluZygpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2Nvcm5lci1oZWFkZXInOlxuICAgICAgICB2YWx1ZSA9ICcnO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIHRocm93ICd1bnJlYWNoYWJsZSc7XG4gICAgfVxuXG4gICAgLy8gUmV0dXJuIHRoZSBmaW5hbCB2YWx1ZS5cbiAgICByZXR1cm4gdmFsdWU7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhpcyBtb2RlbC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX2lzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcblxuICAgIHRoaXMuX2NvbHVtbkNvdW50ID0gdW5kZWZpbmVkO1xuICAgIHRoaXMuX3Jvd0NvdW50ID0gdW5kZWZpbmVkO1xuICAgIHRoaXMuX3Jvd09mZnNldHMgPSBudWxsITtcbiAgICB0aGlzLl9jb2x1bW5PZmZzZXRzID0gbnVsbCE7XG4gICAgdGhpcy5fcmF3RGF0YSA9IG51bGwhO1xuXG4gICAgLy8gQ2xlYXIgb3V0IHN0YXRlIGFzc29jaWF0ZWQgd2l0aCB0aGUgYXN5bmNocm9ub3VzIHBhcnNpbmcuXG4gICAgaWYgKHRoaXMuX2RvbmVQYXJzaW5nID09PSBmYWxzZSkge1xuICAgICAgLy8gRXhwbGljaXRseSBjYXRjaCB0aGlzIHJlamVjdGlvbiBhdCBsZWFzdCBvbmNlIHNvIGFuIGVycm9yIGlzIG5vdCB0aHJvd25cbiAgICAgIC8vIHRvIHRoZSBjb25zb2xlLlxuICAgICAgdGhpcy5yZWFkeS5jYXRjaCgoKSA9PiB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH0pO1xuICAgICAgdGhpcy5fcmVhZHkucmVqZWN0KHVuZGVmaW5lZCk7XG4gICAgfVxuICAgIGlmICh0aGlzLl9kZWxheWVkUGFyc2UgIT09IG51bGwpIHtcbiAgICAgIHdpbmRvdy5jbGVhclRpbWVvdXQodGhpcy5fZGVsYXllZFBhcnNlKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBpbmRleCBpbiB0aGUgZGF0YSBzdHJpbmcgZm9yIHRoZSBmaXJzdCBjaGFyYWN0ZXIgb2YgYSByb3cgYW5kXG4gICAqIGNvbHVtbi5cbiAgICpcbiAgICogQHBhcmFtIHJvdyAtIFRoZSByb3cgb2YgdGhlIGRhdGEgaXRlbS5cbiAgICogQHBhcmFtIGNvbHVtbiAtIFRoZSBjb2x1bW4gb2YgdGhlIGRhdGEgaXRlbS5cbiAgICogQHJldHVybnMgLSBUaGUgaW5kZXggaW50byB0aGUgZGF0YSBzdHJpbmcgd2hlcmUgdGhlIGRhdGEgaXRlbSBzdGFydHMuXG4gICAqL1xuICBnZXRPZmZzZXRJbmRleChyb3c6IG51bWJlciwgY29sdW1uOiBudW1iZXIpOiBudW1iZXIge1xuICAgIC8vIERlY2xhcmUgbG9jYWwgdmFyaWFibGVzLlxuICAgIGNvbnN0IG5jb2xzID0gdGhpcy5fY29sdW1uQ291bnQhO1xuXG4gICAgLy8gQ2hlY2sgdG8gc2VlIGlmIHJvdyAqc2hvdWxkKiBiZSBpbiB0aGUgY2FjaGUsIGJhc2VkIG9uIHRoZSBjYWNoZSBzaXplLlxuICAgIGxldCByb3dJbmRleCA9IChyb3cgLSB0aGlzLl9jb2x1bW5PZmZzZXRzU3RhcnRpbmdSb3cpICogbmNvbHM7XG4gICAgaWYgKHJvd0luZGV4IDwgMCB8fCByb3dJbmRleCA+IHRoaXMuX2NvbHVtbk9mZnNldHMubGVuZ3RoKSB7XG4gICAgICAvLyBSb3cgaXNuJ3QgaW4gdGhlIGNhY2hlLCBzbyB3ZSBpbnZhbGlkYXRlIHRoZSBlbnRpcmUgY2FjaGUgYW5kIHNldCB1cFxuICAgICAgLy8gdGhlIGNhY2hlIHRvIGhvbGQgdGhlIHJlcXVlc3RlZCByb3cuXG4gICAgICB0aGlzLl9jb2x1bW5PZmZzZXRzLmZpbGwoMHhmZmZmZmZmZik7XG4gICAgICB0aGlzLl9jb2x1bW5PZmZzZXRzU3RhcnRpbmdSb3cgPSByb3c7XG4gICAgICByb3dJbmRleCA9IDA7XG4gICAgfVxuXG4gICAgLy8gQ2hlY2sgdG8gc2VlIGlmIHdlIG5lZWQgdG8gZmV0Y2ggdGhlIHJvdyBkYXRhIGludG8gdGhlIGNhY2hlLlxuICAgIGlmICh0aGlzLl9jb2x1bW5PZmZzZXRzW3Jvd0luZGV4XSA9PT0gMHhmZmZmZmZmZikge1xuICAgICAgLy8gRmlndXJlIG91dCBob3cgbWFueSByb3dzIGJlbG93IHVzIGFsc28gbmVlZCB0byBiZSBmZXRjaGVkLlxuICAgICAgbGV0IG1heFJvd3MgPSAxO1xuICAgICAgd2hpbGUgKFxuICAgICAgICBtYXhSb3dzIDw9IHRoaXMuX21heENhY2hlR2V0ICYmXG4gICAgICAgIHRoaXMuX2NvbHVtbk9mZnNldHNbcm93SW5kZXggKyBtYXhSb3dzICogbmNvbHNdID09PSAweGZmZmZmZlxuICAgICAgKSB7XG4gICAgICAgIG1heFJvd3MrKztcbiAgICAgIH1cblxuICAgICAgLy8gUGFyc2UgdGhlIGRhdGEgdG8gZ2V0IHRoZSBjb2x1bW4gb2Zmc2V0cy5cbiAgICAgIGNvbnN0IHsgb2Zmc2V0cyB9ID0gUEFSU0VSU1t0aGlzLl9wYXJzZXJdKHtcbiAgICAgICAgZGF0YTogdGhpcy5fcmF3RGF0YSxcbiAgICAgICAgZGVsaW1pdGVyOiB0aGlzLl9kZWxpbWl0ZXIsXG4gICAgICAgIHJvd0RlbGltaXRlcjogdGhpcy5fcm93RGVsaW1pdGVyLFxuICAgICAgICBxdW90ZTogdGhpcy5fcXVvdGUsXG4gICAgICAgIGNvbHVtbk9mZnNldHM6IHRydWUsXG4gICAgICAgIG1heFJvd3M6IG1heFJvd3MsXG4gICAgICAgIG5jb2xzOiBuY29scyxcbiAgICAgICAgc3RhcnRJbmRleDogdGhpcy5fcm93T2Zmc2V0c1tyb3ddXG4gICAgICB9KTtcblxuICAgICAgLy8gQ29weSByZXN1bHRzIHRvIHRoZSBjYWNoZS5cbiAgICAgIGZvciAobGV0IGkgPSAwOyBpIDwgb2Zmc2V0cy5sZW5ndGg7IGkrKykge1xuICAgICAgICB0aGlzLl9jb2x1bW5PZmZzZXRzW3Jvd0luZGV4ICsgaV0gPSBvZmZzZXRzW2ldO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIFJldHVybiB0aGUgb2Zmc2V0IGluZGV4IGZyb20gY2FjaGUuXG4gICAgcmV0dXJuIHRoaXMuX2NvbHVtbk9mZnNldHNbcm93SW5kZXggKyBjb2x1bW5dO1xuICB9XG5cbiAgLyoqXG4gICAqIFBhcnNlIHRoZSBkYXRhIHN0cmluZyBhc3luY2hyb25vdXNseS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBJdCBjYW4gdGFrZSBzZXZlcmFsIHNlY29uZHMgdG8gcGFyc2UgYSBzZXZlcmFsIGh1bmRyZWQgbWVnYWJ5dGUgc3RyaW5nLCBzb1xuICAgKiB3ZSBwYXJzZSB0aGUgZmlyc3QgNTAwIHJvd3MgdG8gZ2V0IHNvbWV0aGluZyB1cCBvbiB0aGUgc2NyZWVuLCB0aGVuIHdlXG4gICAqIHBhcnNlIHRoZSBmdWxsIGRhdGEgc3RyaW5nIGFzeW5jaHJvbm91c2x5LlxuICAgKi9cbiAgcGFyc2VBc3luYygpOiB2b2lkIHtcbiAgICAvLyBOdW1iZXIgb2Ygcm93cyB0byBnZXQgaW5pdGlhbGx5LlxuICAgIGxldCBjdXJyZW50Um93cyA9IHRoaXMuX2luaXRpYWxSb3dzO1xuXG4gICAgLy8gTnVtYmVyIG9mIHJvd3MgdG8gZ2V0IGluIGVhY2ggY2h1bmsgdGhlcmVhZnRlci4gV2Ugc2V0IHRoaXMgaGlnaCB0byBqdXN0XG4gICAgLy8gZ2V0IHRoZSByZXN0IG9mIHRoZSByb3dzIGZvciBub3cuXG4gICAgbGV0IGNodW5rUm93cyA9IE1hdGgucG93KDIsIDMyKSAtIDE7XG5cbiAgICAvLyBXZSBnaXZlIHRoZSBVSSBhIGNoYW5jZSB0byBkcmF3IGJ5IGRlbGF5aW5nIHRoZSBjaHVuayBwYXJzaW5nLlxuICAgIGNvbnN0IGRlbGF5ID0gMzA7IC8vIG1pbGxpc2Vjb25kc1xuXG4gICAgLy8gRGVmaW5lIGEgZnVuY3Rpb24gdG8gcGFyc2UgYSBjaHVuayB1cCB0byBhbmQgaW5jbHVkaW5nIGVuZFJvdy5cbiAgICBjb25zdCBwYXJzZUNodW5rID0gKGVuZFJvdzogbnVtYmVyKSA9PiB7XG4gICAgICB0cnkge1xuICAgICAgICB0aGlzLl9jb21wdXRlUm93T2Zmc2V0cyhlbmRSb3cpO1xuICAgICAgfSBjYXRjaCAoZSkge1xuICAgICAgICAvLyBTb21ldGltZXMgdGhlIGRhdGEgc3RyaW5nIGNhbm5vdCBiZSBwYXJzZWQgd2l0aCB0aGUgZnVsbCBwYXJzZXIgKGZvclxuICAgICAgICAvLyBleGFtcGxlLCB3ZSBtYXkgaGF2ZSB0aGUgd3JvbmcgZGVsaW1pdGVyKS4gSW4gdGhlc2UgY2FzZXMsIGZhbGwgYmFjayB0b1xuICAgICAgICAvLyB0aGUgc2ltcGxlciBwYXJzZXIgc28gd2UgY2FuIHNob3cgc29tZXRoaW5nLlxuICAgICAgICBpZiAodGhpcy5fcGFyc2VyID09PSAncXVvdGVzJykge1xuICAgICAgICAgIGNvbnNvbGUud2FybihlKTtcbiAgICAgICAgICB0aGlzLl9wYXJzZXIgPSAnbm9xdW90ZXMnO1xuICAgICAgICAgIHRoaXMuX3Jlc2V0UGFyc2VyKCk7XG4gICAgICAgICAgdGhpcy5fY29tcHV0ZVJvd09mZnNldHMoZW5kUm93KTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICB0aHJvdyBlO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICByZXR1cm4gdGhpcy5fZG9uZVBhcnNpbmc7XG4gICAgfTtcblxuICAgIC8vIFJlc2V0IHRoZSBwYXJzZXIgdG8gaXRzIGluaXRpYWwgc3RhdGUuXG4gICAgdGhpcy5fcmVzZXRQYXJzZXIoKTtcblxuICAgIC8vIFBhcnNlIHRoZSBmaXJzdCByb3dzIHRvIGdpdmUgdXMgdGhlIHN0YXJ0IG9mIHRoZSBkYXRhIHJpZ2h0IGF3YXkuXG4gICAgY29uc3QgZG9uZSA9IHBhcnNlQ2h1bmsoY3VycmVudFJvd3MpO1xuXG4gICAgLy8gSWYgd2UgYXJlIGRvbmUsIHJldHVybiBlYXJseS5cbiAgICBpZiAoZG9uZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIC8vIERlZmluZSBhIGZ1bmN0aW9uIHRvIHJlY3Vyc2l2ZWx5IHBhcnNlIHRoZSBuZXh0IGNodW5rIGFmdGVyIGEgZGVsYXkuXG4gICAgY29uc3QgZGVsYXllZFBhcnNlID0gKCkgPT4ge1xuICAgICAgLy8gUGFyc2UgdXAgdG8gdGhlIG5ldyBlbmQgcm93LlxuICAgICAgY29uc3QgZG9uZSA9IHBhcnNlQ2h1bmsoY3VycmVudFJvd3MgKyBjaHVua1Jvd3MpO1xuICAgICAgY3VycmVudFJvd3MgKz0gY2h1bmtSb3dzO1xuXG4gICAgICAvLyBHcmFkdWFsbHkgZG91YmxlIHRoZSBjaHVuayBzaXplIHVudGlsIHdlIHJlYWNoIGEgbWlsbGlvbiByb3dzLCBpZiB3ZVxuICAgICAgLy8gc3RhcnQgYmVsb3cgYSBtaWxsaW9uLXJvdyBjaHVuayBzaXplLlxuICAgICAgaWYgKGNodW5rUm93cyA8IDEwMDAwMDApIHtcbiAgICAgICAgY2h1bmtSb3dzICo9IDI7XG4gICAgICB9XG5cbiAgICAgIC8vIElmIHdlIGFyZW4ndCBkb25lLCB0aGUgc2NoZWR1bGUgYW5vdGhlciBwYXJzZS5cbiAgICAgIGlmIChkb25lKSB7XG4gICAgICAgIHRoaXMuX2RlbGF5ZWRQYXJzZSA9IG51bGw7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB0aGlzLl9kZWxheWVkUGFyc2UgPSB3aW5kb3cuc2V0VGltZW91dChkZWxheWVkUGFyc2UsIGRlbGF5KTtcbiAgICAgIH1cbiAgICB9O1xuXG4gICAgLy8gUGFyc2UgZnVsbCBkYXRhIHN0cmluZyBpbiBjaHVua3MsIGRlbGF5ZWQgYnkgYSBmZXcgbWlsbGlzZWNvbmRzIHRvIGdpdmUgdGhlIFVJIGEgY2hhbmNlIHRvIGRyYXcuXG4gICAgdGhpcy5fZGVsYXllZFBhcnNlID0gd2luZG93LnNldFRpbWVvdXQoZGVsYXllZFBhcnNlLCBkZWxheSk7XG4gIH1cblxuICAvKipcbiAgICogQ29tcHV0ZSB0aGUgcm93IG9mZnNldHMgYW5kIGluaXRpYWxpemUgdGhlIGNvbHVtbiBvZmZzZXQgY2FjaGUuXG4gICAqXG4gICAqIEBwYXJhbSBlbmRSb3cgLSBUaGUgbGFzdCByb3cgdG8gcGFyc2UsIGZyb20gdGhlIHN0YXJ0IG9mIHRoZSBkYXRhIChmaXJzdFxuICAgKiByb3cgaXMgcm93IDEpLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgbWV0aG9kIHN1cHBvcnRzIHBhcnNpbmcgdGhlIGRhdGEgaW5jcmVtZW50YWxseSBieSBjYWxsaW5nIGl0IHdpdGhcbiAgICogaW5jcmVtZW50YWxseSBoaWdoZXIgZW5kUm93LiBSb3dzIHRoYXQgaGF2ZSBhbHJlYWR5IGJlZW4gcGFyc2VkIHdpbGwgbm90IGJlXG4gICAqIHBhcnNlZCBhZ2Fpbi5cbiAgICovXG4gIHByaXZhdGUgX2NvbXB1dGVSb3dPZmZzZXRzKGVuZFJvdyA9IDQyOTQ5NjcyOTUpOiB2b2lkIHtcbiAgICAvLyBJZiB3ZSd2ZSBhbHJlYWR5IHBhcnNlZCB1cCB0byBlbmRSb3csIG9yIGlmIHdlJ3ZlIGFscmVhZHkgcGFyc2VkIHRoZVxuICAgIC8vIGVudGlyZSBkYXRhIHNldCwgcmV0dXJuIGVhcmx5LlxuICAgIGlmICh0aGlzLl9yb3dDb3VudCEgPj0gZW5kUm93IHx8IHRoaXMuX2RvbmVQYXJzaW5nID09PSB0cnVlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gQ29tcHV0ZSB0aGUgY29sdW1uIGNvdW50IGlmIHdlIGRvbid0IGFscmVhZHkgaGF2ZSBpdC5cbiAgICBpZiAodGhpcy5fY29sdW1uQ291bnQgPT09IHVuZGVmaW5lZCkge1xuICAgICAgLy8gR2V0IG51bWJlciBvZiBjb2x1bW5zIGluIGZpcnN0IHJvd1xuICAgICAgdGhpcy5fY29sdW1uQ291bnQgPSBQQVJTRVJTW3RoaXMuX3BhcnNlcl0oe1xuICAgICAgICBkYXRhOiB0aGlzLl9yYXdEYXRhLFxuICAgICAgICBkZWxpbWl0ZXI6IHRoaXMuX2RlbGltaXRlcixcbiAgICAgICAgcm93RGVsaW1pdGVyOiB0aGlzLl9yb3dEZWxpbWl0ZXIsXG4gICAgICAgIHF1b3RlOiB0aGlzLl9xdW90ZSxcbiAgICAgICAgY29sdW1uT2Zmc2V0czogdHJ1ZSxcbiAgICAgICAgbWF4Um93czogMVxuICAgICAgfSkubmNvbHM7XG4gICAgfVxuXG4gICAgLy8gYHJlcGFyc2VgIGlzIHRoZSBudW1iZXIgb2Ygcm93cyB3ZSBhcmUgcmVxdWVzdGluZyB0byBwYXJzZSBvdmVyIGFnYWluLlxuICAgIC8vIFdlIGdlbmVyYWxseSBzdGFydCBhdCB0aGUgYmVnaW5uaW5nIG9mIHRoZSBsYXN0IHJvdyBvZmZzZXQsIHNvIHRoYXQgdGhlXG4gICAgLy8gZmlyc3Qgcm93IG9mZnNldCByZXR1cm5lZCBpcyB0aGUgc2FtZSBhcyB0aGUgbGFzdCByb3cgb2Zmc2V0IHdlIGFscmVhZHlcbiAgICAvLyBoYXZlLiBXZSBwYXJzZSB0aGUgZGF0YSB1cCB0byBhbmQgaW5jbHVkaW5nIHRoZSByZXF1ZXN0ZWQgcm93LlxuICAgIGNvbnN0IHJlcGFyc2UgPSB0aGlzLl9yb3dDb3VudCEgPiAwID8gMSA6IDA7XG4gICAgY29uc3QgeyBucm93cywgb2Zmc2V0cyB9ID0gUEFSU0VSU1t0aGlzLl9wYXJzZXJdKHtcbiAgICAgIGRhdGE6IHRoaXMuX3Jhd0RhdGEsXG4gICAgICBzdGFydEluZGV4OiB0aGlzLl9yb3dPZmZzZXRzW3RoaXMuX3Jvd0NvdW50ISAtIHJlcGFyc2VdID8/IDAsXG4gICAgICBkZWxpbWl0ZXI6IHRoaXMuX2RlbGltaXRlcixcbiAgICAgIHJvd0RlbGltaXRlcjogdGhpcy5fcm93RGVsaW1pdGVyLFxuICAgICAgcXVvdGU6IHRoaXMuX3F1b3RlLFxuICAgICAgY29sdW1uT2Zmc2V0czogZmFsc2UsXG4gICAgICBtYXhSb3dzOiBlbmRSb3cgLSB0aGlzLl9yb3dDb3VudCEgKyByZXBhcnNlXG4gICAgfSk7XG5cbiAgICAvLyBJZiB3ZSBoYXZlIGFscmVhZHkgc2V0IHVwIG91ciBpbml0aWFsIGJvb2trZWVwaW5nLCByZXR1cm4gZWFybHkgaWYgd2VcbiAgICAvLyBkaWQgbm90IGdldCBhbnkgbmV3IHJvd3MgYmV5b25kIHRoZSBsYXN0IHJvdyB0aGF0IHdlJ3ZlIHBhcnNlZCwgaS5lLixcbiAgICAvLyBucm93cz09PTEuXG4gICAgaWYgKHRoaXMuX3N0YXJ0ZWRQYXJzaW5nICYmIG5yb3dzIDw9IHJlcGFyc2UpIHtcbiAgICAgIHRoaXMuX2RvbmVQYXJzaW5nID0gdHJ1ZTtcbiAgICAgIHRoaXMuX3JlYWR5LnJlc29sdmUodW5kZWZpbmVkKTtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aGlzLl9zdGFydGVkUGFyc2luZyA9IHRydWU7XG5cbiAgICAvLyBVcGRhdGUgdGhlIHJvdyBjb3VudCwgYWNjb3VudGluZyBmb3IgaG93IG1hbnkgcm93cyB3ZXJlIHJlcGFyc2VkLlxuICAgIGNvbnN0IG9sZFJvd0NvdW50ID0gdGhpcy5fcm93Q291bnQhO1xuICAgIGNvbnN0IGR1cGxpY2F0ZVJvd3MgPSBNYXRoLm1pbihucm93cywgcmVwYXJzZSk7XG4gICAgdGhpcy5fcm93Q291bnQgPSBvbGRSb3dDb3VudCArIG5yb3dzIC0gZHVwbGljYXRlUm93cztcblxuICAgIC8vIElmIHdlIGRpZG4ndCByZWFjaCB0aGUgcmVxdWVzdGVkIHJvdywgd2UgbXVzdCBiZSBkb25lLlxuICAgIGlmICh0aGlzLl9yb3dDb3VudCA8IGVuZFJvdykge1xuICAgICAgdGhpcy5fZG9uZVBhcnNpbmcgPSB0cnVlO1xuICAgICAgdGhpcy5fcmVhZHkucmVzb2x2ZSh1bmRlZmluZWQpO1xuICAgIH1cblxuICAgIC8vIENvcHkgdGhlIG5ldyBvZmZzZXRzIGludG8gYSBuZXcgcm93IG9mZnNldCBhcnJheSBpZiBuZWVkZWQuXG4gICAgaWYgKHRoaXMuX3Jvd0NvdW50ID4gb2xkUm93Q291bnQpIHtcbiAgICAgIGNvbnN0IG9sZFJvd09mZnNldHMgPSB0aGlzLl9yb3dPZmZzZXRzO1xuICAgICAgdGhpcy5fcm93T2Zmc2V0cyA9IG5ldyBVaW50MzJBcnJheSh0aGlzLl9yb3dDb3VudCk7XG4gICAgICB0aGlzLl9yb3dPZmZzZXRzLnNldChvbGRSb3dPZmZzZXRzKTtcbiAgICAgIHRoaXMuX3Jvd09mZnNldHMuc2V0KG9mZnNldHMsIG9sZFJvd0NvdW50IC0gZHVwbGljYXRlUm93cyk7XG4gICAgfVxuXG4gICAgLy8gRXhwYW5kIHRoZSBjb2x1bW4gb2Zmc2V0cyBhcnJheSBpZiBuZWVkZWRcblxuICAgIC8vIElmIHRoZSBmdWxsIGNvbHVtbiBvZmZzZXRzIGFycmF5IGlzIHNtYWxsIGVub3VnaCwgYnVpbGQgYSBjYWNoZSBiaWdcbiAgICAvLyBlbm91Z2ggZm9yIGFsbCBjb2x1bW4gb2Zmc2V0cy4gV2UgYWxsb2NhdGUgdXAgdG8gMTI4IG1lZ2FieXRlczpcbiAgICAvLyAxMjgqKDIqKjIwIGJ5dGVzL00pLyg0IGJ5dGVzL2VudHJ5KSA9IDMzNTU0NDMyIGVudHJpZXMuXG4gICAgY29uc3QgbWF4Q29sdW1uT2Zmc2V0c1Jvd3MgPSBNYXRoLmZsb29yKDMzNTU0NDMyIC8gdGhpcy5fY29sdW1uQ291bnQpO1xuXG4gICAgLy8gV2UgbmVlZCB0byBleHBhbmQgdGhlIGNvbHVtbiBvZmZzZXQgYXJyYXkgaWYgd2Ugd2VyZSBzdG9yaW5nIGFsbCBjb2x1bW5cbiAgICAvLyBvZmZzZXRzIGJlZm9yZS4gQ2hlY2sgdG8gc2VlIGlmIHRoZSBwcmV2aW91cyBzaXplIHdhcyBzbWFsbCBlbm91Z2ggdGhhdFxuICAgIC8vIHdlIHN0b3JlZCBhbGwgY29sdW1uIG9mZnNldHMuXG4gICAgaWYgKG9sZFJvd0NvdW50IDw9IG1heENvbHVtbk9mZnNldHNSb3dzKSB7XG4gICAgICAvLyBDaGVjayB0byBzZWUgaWYgdGhlIG5ldyBjb2x1bW4gb2Zmc2V0cyBhcnJheSBpcyBzbWFsbCBlbm91Z2ggdG8gc3RpbGxcbiAgICAgIC8vIHN0b3JlLCBvciBpZiB3ZSBzaG91bGQgY3V0IG92ZXIgdG8gYSBzbWFsbCBjYWNoZS5cbiAgICAgIGlmICh0aGlzLl9yb3dDb3VudCA8PSBtYXhDb2x1bW5PZmZzZXRzUm93cykge1xuICAgICAgICAvLyBFeHBhbmQgdGhlIGV4aXN0aW5nIGNvbHVtbiBvZmZzZXQgYXJyYXkgZm9yIG5ldyBjb2x1bW4gb2Zmc2V0cy5cbiAgICAgICAgY29uc3Qgb2xkQ29sdW1uT2Zmc2V0cyA9IHRoaXMuX2NvbHVtbk9mZnNldHM7XG4gICAgICAgIHRoaXMuX2NvbHVtbk9mZnNldHMgPSBuZXcgVWludDMyQXJyYXkoXG4gICAgICAgICAgdGhpcy5fcm93Q291bnQgKiB0aGlzLl9jb2x1bW5Db3VudFxuICAgICAgICApO1xuICAgICAgICB0aGlzLl9jb2x1bW5PZmZzZXRzLnNldChvbGRDb2x1bW5PZmZzZXRzKTtcbiAgICAgICAgdGhpcy5fY29sdW1uT2Zmc2V0cy5maWxsKDB4ZmZmZmZmZmYsIG9sZENvbHVtbk9mZnNldHMubGVuZ3RoKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIC8vIElmIG5vdCwgdGhlbiBvdXIgY2FjaGUgc2l6ZSBpcyBhdCBtb3N0IHRoZSBtYXhpbXVtIG51bWJlciBvZiByb3dzIHdlXG4gICAgICAgIC8vIGZpbGwgaW4gdGhlIGNhY2hlIGF0IGEgdGltZS5cbiAgICAgICAgY29uc3Qgb2xkQ29sdW1uT2Zmc2V0cyA9IHRoaXMuX2NvbHVtbk9mZnNldHM7XG4gICAgICAgIHRoaXMuX2NvbHVtbk9mZnNldHMgPSBuZXcgVWludDMyQXJyYXkoXG4gICAgICAgICAgTWF0aC5taW4odGhpcy5fbWF4Q2FjaGVHZXQsIG1heENvbHVtbk9mZnNldHNSb3dzKSAqIHRoaXMuX2NvbHVtbkNvdW50XG4gICAgICAgICk7XG5cbiAgICAgICAgLy8gRmlsbCBpbiB0aGUgZW50cmllcyB3ZSBhbHJlYWR5IGhhdmUuXG4gICAgICAgIHRoaXMuX2NvbHVtbk9mZnNldHMuc2V0KFxuICAgICAgICAgIG9sZENvbHVtbk9mZnNldHMuc3ViYXJyYXkoMCwgdGhpcy5fY29sdW1uT2Zmc2V0cy5sZW5ndGgpXG4gICAgICAgICk7XG5cbiAgICAgICAgLy8gSW52YWxpZGF0ZSB0aGUgcmVzdCBvZiB0aGUgZW50cmllcy5cbiAgICAgICAgdGhpcy5fY29sdW1uT2Zmc2V0cy5maWxsKDB4ZmZmZmZmZmYsIG9sZENvbHVtbk9mZnNldHMubGVuZ3RoKTtcbiAgICAgICAgdGhpcy5fY29sdW1uT2Zmc2V0c1N0YXJ0aW5nUm93ID0gMDtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyBXZSBoYXZlIG1vcmUgcm93cyB0aGFuIGJlZm9yZSwgc28gZW1pdCB0aGUgcm93cy1pbnNlcnRlZCBjaGFuZ2Ugc2lnbmFsLlxuICAgIGxldCBmaXJzdEluZGV4ID0gb2xkUm93Q291bnQ7XG4gICAgaWYgKHRoaXMuX2hlYWRlci5sZW5ndGggPiAwKSB7XG4gICAgICBmaXJzdEluZGV4IC09IDE7XG4gICAgfVxuICAgIHRoaXMuZW1pdENoYW5nZWQoe1xuICAgICAgdHlwZTogJ3Jvd3MtaW5zZXJ0ZWQnLFxuICAgICAgcmVnaW9uOiAnYm9keScsXG4gICAgICBpbmRleDogZmlyc3RJbmRleCxcbiAgICAgIHNwYW46IHRoaXMuX3Jvd0NvdW50IC0gb2xkUm93Q291bnRcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHBhcnNlZCBzdHJpbmcgZmllbGQgZm9yIGEgcm93IGFuZCBjb2x1bW4uXG4gICAqXG4gICAqIEBwYXJhbSByb3cgLSBUaGUgcm93IG51bWJlciBvZiB0aGUgZGF0YSBpdGVtLlxuICAgKiBAcGFyYW0gY29sdW1uIC0gVGhlIGNvbHVtbiBudW1iZXIgb2YgdGhlIGRhdGEgaXRlbS5cbiAgICogQHJldHVybnMgVGhlIHBhcnNlZCBzdHJpbmcgZm9yIHRoZSBkYXRhIGl0ZW0uXG4gICAqL1xuICBwcml2YXRlIF9nZXRGaWVsZChyb3c6IG51bWJlciwgY29sdW1uOiBudW1iZXIpOiBzdHJpbmcge1xuICAgIC8vIERlY2xhcmUgbG9jYWwgdmFyaWFibGVzLlxuICAgIGxldCB2YWx1ZTogc3RyaW5nO1xuICAgIGxldCBuZXh0SW5kZXg7XG5cbiAgICAvLyBGaW5kIHRoZSBpbmRleCBmb3IgdGhlIGZpcnN0IGNoYXJhY3RlciBpbiB0aGUgZmllbGQuXG4gICAgY29uc3QgaW5kZXggPSB0aGlzLmdldE9mZnNldEluZGV4KHJvdywgY29sdW1uKTtcblxuICAgIC8vIEluaXRpYWxpemUgdGhlIHRyaW0gYWRqdXN0bWVudHMuXG4gICAgbGV0IHRyaW1SaWdodCA9IDA7XG4gICAgbGV0IHRyaW1MZWZ0ID0gMDtcblxuICAgIC8vIEZpbmQgdGhlIGVuZCBvZiB0aGUgc2xpY2UgKHRoZSBzdGFydCBvZiB0aGUgbmV4dCBmaWVsZCksIGFuZCBob3cgbXVjaCB3ZVxuICAgIC8vIHNob3VsZCBhZGp1c3QgdG8gdHJpbSBvZmYgYSB0cmFpbGluZyBmaWVsZCBvciByb3cgZGVsaW1pdGVyLiBGaXJzdCBjaGVja1xuICAgIC8vIGlmIHdlIGFyZSBnZXR0aW5nIHRoZSBsYXN0IGNvbHVtbi5cbiAgICBpZiAoY29sdW1uID09PSB0aGlzLl9jb2x1bW5Db3VudCEgLSAxKSB7XG4gICAgICAvLyBDaGVjayBpZiB3ZSBhcmUgZ2V0dGluZyBhbnkgcm93IGJ1dCB0aGUgbGFzdC5cbiAgICAgIGlmIChyb3cgPCB0aGlzLl9yb3dDb3VudCEgLSAxKSB7XG4gICAgICAgIC8vIFNldCB0aGUgbmV4dCBvZmZzZXQgdG8gdGhlIG5leHQgcm93LCBjb2x1bW4gMC5cbiAgICAgICAgbmV4dEluZGV4ID0gdGhpcy5nZXRPZmZzZXRJbmRleChyb3cgKyAxLCAwKTtcblxuICAgICAgICAvLyBTaW5jZSB3ZSBhcmUgbm90IGF0IHRoZSBsYXN0IHJvdywgd2UgbmVlZCB0byB0cmltIG9mZiB0aGUgcm93XG4gICAgICAgIC8vIGRlbGltaXRlci5cbiAgICAgICAgdHJpbVJpZ2h0ICs9IHRoaXMuX3Jvd0RlbGltaXRlci5sZW5ndGg7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICAvLyBXZSBhcmUgZ2V0dGluZyB0aGUgbGFzdCBkYXRhIGl0ZW0sIHNvIHRoZSBzbGljZSBlbmQgaXMgdGhlIGVuZCBvZiB0aGVcbiAgICAgICAgLy8gZGF0YSBzdHJpbmcuXG4gICAgICAgIG5leHRJbmRleCA9IHRoaXMuX3Jhd0RhdGEubGVuZ3RoO1xuXG4gICAgICAgIC8vIFRoZSBzdHJpbmcgbWF5IG9yIG1heSBub3QgZW5kIGluIGEgcm93IGRlbGltaXRlciAoUkZDIDQxODAgMi4yKSwgc29cbiAgICAgICAgLy8gd2UgZXhwbGljaXRseSBjaGVjayBpZiB3ZSBzaG91bGQgdHJpbSBvZmYgYSByb3cgZGVsaW1pdGVyLlxuICAgICAgICBpZiAoXG4gICAgICAgICAgdGhpcy5fcmF3RGF0YVtuZXh0SW5kZXggLSAxXSA9PT1cbiAgICAgICAgICB0aGlzLl9yb3dEZWxpbWl0ZXJbdGhpcy5fcm93RGVsaW1pdGVyLmxlbmd0aCAtIDFdXG4gICAgICAgICkge1xuICAgICAgICAgIHRyaW1SaWdodCArPSB0aGlzLl9yb3dEZWxpbWl0ZXIubGVuZ3RoO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIC8vIFRoZSBuZXh0IGZpZWxkIHN0YXJ0cyBhdCB0aGUgbmV4dCBjb2x1bW4gb2Zmc2V0LlxuICAgICAgbmV4dEluZGV4ID0gdGhpcy5nZXRPZmZzZXRJbmRleChyb3csIGNvbHVtbiArIDEpO1xuXG4gICAgICAvLyBUcmltIG9mZiB0aGUgZGVsaW1pdGVyIGlmIGl0IGV4aXN0cyBhdCB0aGUgZW5kIG9mIHRoZSBmaWVsZFxuICAgICAgaWYgKFxuICAgICAgICBpbmRleCA8IG5leHRJbmRleCAmJlxuICAgICAgICB0aGlzLl9yYXdEYXRhW25leHRJbmRleCAtIDFdID09PSB0aGlzLl9kZWxpbWl0ZXJcbiAgICAgICkge1xuICAgICAgICB0cmltUmlnaHQgKz0gMTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyBDaGVjayB0byBzZWUgaWYgdGhlIGZpZWxkIGJlZ2lucyB3aXRoIGEgcXVvdGUuIElmIGl0IGRvZXMsIHRyaW0gYSBxdW90ZSBvbiBlaXRoZXIgc2lkZS5cbiAgICBpZiAodGhpcy5fcmF3RGF0YVtpbmRleF0gPT09IHRoaXMuX3F1b3RlKSB7XG4gICAgICB0cmltTGVmdCArPSAxO1xuICAgICAgdHJpbVJpZ2h0ICs9IDE7XG4gICAgfVxuXG4gICAgLy8gU2xpY2UgdGhlIGFjdHVhbCB2YWx1ZSBvdXQgb2YgdGhlIGRhdGEgc3RyaW5nLlxuICAgIHZhbHVlID0gdGhpcy5fcmF3RGF0YS5zbGljZShpbmRleCArIHRyaW1MZWZ0LCBuZXh0SW5kZXggLSB0cmltUmlnaHQpO1xuXG4gICAgLy8gSWYgd2UgaGF2ZSBhIHF1b3RlZCBmaWVsZCBhbmQgd2UgaGF2ZSBhbiBlc2NhcGVkIHF1b3RlIGluc2lkZSBpdCwgdW5lc2NhcGUgaXQuXG4gICAgaWYgKHRyaW1MZWZ0ID09PSAxICYmIHZhbHVlLmluZGV4T2YodGhpcy5fcXVvdGUpICE9PSAtMSkge1xuICAgICAgdmFsdWUgPSB2YWx1ZS5yZXBsYWNlKHRoaXMuX3F1b3RlRXNjYXBlZCwgdGhpcy5fcXVvdGUpO1xuICAgIH1cblxuICAgIC8vIFJldHVybiB0aGUgdmFsdWUuXG4gICAgcmV0dXJuIHZhbHVlO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlc2V0IHRoZSBwYXJzZXIgc3RhdGUuXG4gICAqL1xuICBwcml2YXRlIF9yZXNldFBhcnNlcigpOiB2b2lkIHtcbiAgICB0aGlzLl9jb2x1bW5Db3VudCA9IHVuZGVmaW5lZDtcblxuICAgIHRoaXMuX3Jvd09mZnNldHMgPSBuZXcgVWludDMyQXJyYXkoMCk7XG4gICAgdGhpcy5fcm93Q291bnQgPSAwO1xuICAgIHRoaXMuX3N0YXJ0ZWRQYXJzaW5nID0gZmFsc2U7XG5cbiAgICB0aGlzLl9jb2x1bW5PZmZzZXRzID0gbmV3IFVpbnQzMkFycmF5KDApO1xuXG4gICAgLy8gQ2xlYXIgb3V0IHN0YXRlIGFzc29jaWF0ZWQgd2l0aCB0aGUgYXN5bmNocm9ub3VzIHBhcnNpbmcuXG4gICAgaWYgKHRoaXMuX2RvbmVQYXJzaW5nID09PSBmYWxzZSkge1xuICAgICAgLy8gRXhwbGljaXRseSBjYXRjaCB0aGlzIHJlamVjdGlvbiBhdCBsZWFzdCBvbmNlIHNvIGFuIGVycm9yIGlzIG5vdCB0aHJvd25cbiAgICAgIC8vIHRvIHRoZSBjb25zb2xlLlxuICAgICAgdGhpcy5yZWFkeS5jYXRjaCgoKSA9PiB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH0pO1xuICAgICAgdGhpcy5fcmVhZHkucmVqZWN0KHVuZGVmaW5lZCk7XG4gICAgfVxuICAgIHRoaXMuX2RvbmVQYXJzaW5nID0gZmFsc2U7XG4gICAgdGhpcy5fcmVhZHkgPSBuZXcgUHJvbWlzZURlbGVnYXRlPHZvaWQ+KCk7XG4gICAgaWYgKHRoaXMuX2RlbGF5ZWRQYXJzZSAhPT0gbnVsbCkge1xuICAgICAgd2luZG93LmNsZWFyVGltZW91dCh0aGlzLl9kZWxheWVkUGFyc2UpO1xuICAgICAgdGhpcy5fZGVsYXllZFBhcnNlID0gbnVsbDtcbiAgICB9XG5cbiAgICB0aGlzLmVtaXRDaGFuZ2VkKHsgdHlwZTogJ21vZGVsLXJlc2V0JyB9KTtcbiAgfVxuXG4gIC8vIFBhcnNlciBzZXR0aW5nc1xuICBwcml2YXRlIF9kZWxpbWl0ZXI6IHN0cmluZztcbiAgcHJpdmF0ZSBfcXVvdGU6IHN0cmluZztcbiAgcHJpdmF0ZSBfcXVvdGVFc2NhcGVkOiBSZWdFeHA7XG4gIHByaXZhdGUgX3BhcnNlcjogJ3F1b3RlcycgfCAnbm9xdW90ZXMnO1xuICBwcml2YXRlIF9yb3dEZWxpbWl0ZXI6IHN0cmluZztcblxuICAvLyBEYXRhIHZhbHVlc1xuICBwcml2YXRlIF9yYXdEYXRhOiBzdHJpbmc7XG4gIHByaXZhdGUgX3Jvd0NvdW50OiBudW1iZXIgfCB1bmRlZmluZWQgPSAwO1xuICBwcml2YXRlIF9jb2x1bW5Db3VudDogbnVtYmVyIHwgdW5kZWZpbmVkO1xuXG4gIC8vIENhY2hlIGluZm9ybWF0aW9uXG4gIC8qKlxuICAgKiBUaGUgaGVhZGVyIHN0cmluZ3MuXG4gICAqL1xuICBwcml2YXRlIF9oZWFkZXI6IHN0cmluZ1tdID0gW107XG4gIC8qKlxuICAgKiBUaGUgY29sdW1uIG9mZnNldCBjYWNoZSwgc3RhcnRpbmcgd2l0aCByb3cgX2NvbHVtbk9mZnNldHNTdGFydGluZ1Jvd1xuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBpbmRleCBvZiB0aGUgZmlyc3QgY2hhcmFjdGVyIGluIHRoZSBkYXRhIHN0cmluZyBmb3Igcm93IHIsIGNvbHVtbiBjIGlzXG4gICAqIF9jb2x1bW5PZmZzZXRzWyhyLXRoaXMuX2NvbHVtbk9mZnNldHNTdGFydGluZ1JvdykqbnVtQ29sdW1ucytjXVxuICAgKi9cbiAgcHJpdmF0ZSBfY29sdW1uT2Zmc2V0czogVWludDMyQXJyYXkgPSBuZXcgVWludDMyQXJyYXkoMCk7XG4gIC8qKlxuICAgKiBUaGUgcm93IHRoYXQgX2NvbHVtbk9mZnNldHNbMF0gcmVwcmVzZW50cy5cbiAgICovXG4gIHByaXZhdGUgX2NvbHVtbk9mZnNldHNTdGFydGluZ1JvdzogbnVtYmVyID0gMDtcbiAgLyoqXG4gICAqIFRoZSBtYXhpbXVtIG51bWJlciBvZiByb3dzIHRvIHBhcnNlIHdoZW4gdGhlcmUgaXMgYSBjYWNoZSBtaXNzLlxuICAgKi9cbiAgcHJpdmF0ZSBfbWF4Q2FjaGVHZXQ6IG51bWJlciA9IDEwMDA7XG4gIC8qKlxuICAgKiBUaGUgaW5kZXggZm9yIHRoZSBzdGFydCBvZiBlYWNoIHJvdy5cbiAgICovXG4gIHByaXZhdGUgX3Jvd09mZnNldHM6IFVpbnQzMkFycmF5ID0gbmV3IFVpbnQzMkFycmF5KDApO1xuICAvKipcbiAgICogVGhlIG51bWJlciBvZiByb3dzIHRvIHBhcnNlIGluaXRpYWxseSBiZWZvcmUgZG9pbmcgYSBkZWxheWVkIHBhcnNlIG9mIHRoZVxuICAgKiBlbnRpcmUgZGF0YS5cbiAgICovXG4gIHByaXZhdGUgX2luaXRpYWxSb3dzOiBudW1iZXI7XG5cbiAgLy8gQm9va2tlZXBpbmcgdmFyaWFibGVzLlxuICBwcml2YXRlIF9kZWxheWVkUGFyc2U6IG51bWJlciB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9zdGFydGVkUGFyc2luZzogYm9vbGVhbiA9IGZhbHNlO1xuICBwcml2YXRlIF9kb25lUGFyc2luZzogYm9vbGVhbiA9IGZhbHNlO1xuICBwcml2YXRlIF9pc0Rpc3Bvc2VkOiBib29sZWFuID0gZmFsc2U7XG4gIHByaXZhdGUgX3JlYWR5ID0gbmV3IFByb21pc2VEZWxlZ2F0ZTx2b2lkPigpO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIHRoZSBgRFNWTW9kZWxgIGNsYXNzIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgRFNWTW9kZWwge1xuICAvKipcbiAgICogQW4gb3B0aW9ucyBvYmplY3QgZm9yIGluaXRpYWxpemluZyBhIGRlbGltaXRlci1zZXBhcmF0ZWQgZGF0YSBtb2RlbC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBmaWVsZCBkZWxpbWl0ZXIsIHN1Y2ggYXMgJywnIG9yICdcXHQnLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFRoZSBmaWVsZCBkZWxpbWl0ZXIgbXVzdCBiZSBhIHNpbmdsZSBjaGFyYWN0ZXIuXG4gICAgICovXG4gICAgZGVsaW1pdGVyOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZGF0YSBzb3VyY2UgZm9yIHRoZSBkYXRhIG1vZGVsLlxuICAgICAqL1xuICAgIGRhdGE6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdGhlIGRhdGEgaGFzIGEgb25lLXJvdyBoZWFkZXIuXG4gICAgICovXG4gICAgaGVhZGVyPzogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFJvdyBkZWxpbWl0ZXIuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogQW55IGNhcnJpYWdlIHJldHVybiBvciBuZXdsaW5lIGNoYXJhY3RlciB0aGF0IGlzIG5vdCBhIGRlbGltaXRlciBzaG91bGRcbiAgICAgKiBiZSBpbiBhIHF1b3RlZCBmaWVsZCwgcmVnYXJkbGVzcyBvZiB0aGUgcm93IGRlbGltaXRlciBzZXR0aW5nLlxuICAgICAqL1xuICAgIHJvd0RlbGltaXRlcj86ICdcXHJcXG4nIHwgJ1xccicgfCAnXFxuJztcblxuICAgIC8qKlxuICAgICAqIFF1b3RlIGNoYXJhY3Rlci5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBRdW90ZXMgYXJlIGVzY2FwZWQgYnkgcmVwZWF0aW5nIHRoZW0sIGFzIGluIFJGQyA0MTgwLiBUaGUgcXVvdGUgbXVzdCBiZSBhXG4gICAgICogc2luZ2xlIGNoYXJhY3Rlci5cbiAgICAgKi9cbiAgICBxdW90ZT86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gdXNlIHRoZSBwYXJzZXIgdGhhdCBjYW4gaGFuZGxlIHF1b3RlZCBkZWxpbWl0ZXJzLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFNldHRpbmcgdGhpcyB0byBmYWxzZSB1c2VzIGEgbXVjaCBmYXN0ZXIgcGFyc2VyLCBidXQgYXNzdW1lcyB0aGVyZSBhcmVcbiAgICAgKiBub3QgYW55IGZpZWxkIG9yIHJvdyBkZWxpbWl0ZXJzIHRoYXQgYXJlIHF1b3RlZCBpbiBmaWVsZHMuIElmIHRoaXMgaXMgbm90XG4gICAgICogc2V0LCBpdCBkZWZhdWx0cyB0byB0cnVlIGlmIGFueSBxdW90ZXMgYXJlIGZvdW5kIGluIHRoZSBkYXRhLCBhbmQgZmFsc2VcbiAgICAgKiBvdGhlcndpc2UuXG4gICAgICovXG4gICAgcXVvdGVQYXJzZXI/OiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG1heGltdW0gbnVtYmVyIG9mIGluaXRpYWwgcm93cyB0byBwYXJzZSBiZWZvcmUgZG9pbmcgYSBhc3luY2hyb25vdXNcbiAgICAgKiBmdWxsIHBhcnNlIG9mIHRoZSBkYXRhLiBUaGlzIHNob3VsZCBiZSBncmVhdGVyIHRoYW4gMC5cbiAgICAgKi9cbiAgICBpbml0aWFsUm93cz86IG51bWJlcjtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG4vKlxuUG9zc2libGUgb3B0aW9ucyB0byBhZGQgdG8gdGhlIHBhcnNlcjpcblxuLSBPcHRpb25hbCBvZmZzZXRzIGFycmF5IHRvIG1vZGlmeSwgc28gd2UgZG9uJ3QgbmVlZCB0byBjcmVhdGUgYSBuZXcgb2Zmc2V0cyBsaXN0ICh3ZSB3b3VsZCBuZWVkIHRvIGJlIGNhcmVmdWwgbm90IHRvIG92ZXJ3cml0ZSB0aGluZ3MgaWYgYSByb3cgbmVlZHMgdG8gYmUgdHJ1bmNhdGVkLilcbi0gQ29tbWVudCBjaGFyYWN0ZXIgYXQgdGhlIHN0YXJ0IG9mIHRoZSBsaW5lXG4tIFNraXAgZW1wdHkgd2hpdGVzcGFjZSBsaW5lc1xuLSBTa2lwIHJvd3Mgd2l0aCBlbXB0eSBjb2x1bW5zXG4tIExvZ2dpbmcgYW4gZXJyb3IgZm9yIHRvbyBtYW55IG9yIHRvbyBmZXcgZmllbGRzIG9uIGEgbGluZVxuLSBJZ25vcmUgd2hpdGVzcGFjZSBhcm91bmQgZGVsaW1pdGVyc1xuLSBBZGQgYW4gZXhwb3J0ZWQgZnVuY3Rpb24gaW4gdGhpcyBmaWxlIGZvciBnZXR0aW5nIGEgZmllbGQgZnJvbSB0aGUgcmV0dXJuZWQgb2Zmc2V0cyBhcnJheSAoaW5jbHVkaW5nIHN0cmlwcGluZyBmaWVsZCBvciByb3cgZGVsaW1pdGVycyBhbmQgcGFyc2luZyBxdW90ZWQgZGF0YSkuIFJpZ2h0IG5vdyB0aGlzIGxvZ2ljIGlzIGluIHRoZSBEU1ZNb2RlbC4gTGlrZWx5IHdlIHdhbnQgdG8ga2VlcCB0aGUgbG9naWMgdGhlcmUgZm9yIHNwZWVkLCBidXQgaGF2aW5nIGl0IGhlcmUgYXMgd2VsbCB3aWxsIG1ha2UgdGhlIHBhcnNlciBtb3JlIHNlbGYtY29udGFpbmVkIGFuZCB1c2FibGUgYnkgb3RoZXJzLlxuLSBTYW5pdHkgY2hlY2sgb24gZmllbGQgc2l6ZSwgd2l0aCBhbiBlcnJvciBpZiB0aGUgZmllbGQgZXhjZWVkcyB0aGUgc2l6ZVxuLSBUZXN0cyBhZ2FpbnN0IGh0dHBzOi8vZ2l0aHViLmNvbS9tYXhvZ2Rlbi9jc3Ytc3BlY3RydW1cbi0gQmVuY2htYXJrIGFnYWluc3QgaHR0cHM6Ly93d3cubnBtanMuY29tL3BhY2thZ2UvY3N2LXBhcnNlciBhbmQgaHR0cHM6Ly93d3cubnBtanMuY29tL3BhY2thZ2UvY3N2LXN0cmluZyBhbmQgZmFzdC1jc3YuXG5cbiovXG5cbi8qKlxuICogSW50ZXJmYWNlIGZvciBhIGRlbGltaXRlci1zZXBhcmF0ZWQgZGF0YSBwYXJzZXIuXG4gKlxuICogQHBhcmFtIG9wdGlvbnM6IFRoZSBwYXJzZXIgb3B0aW9uc1xuICogQHJldHVybnMgQW4gb2JqZWN0IGdpdmluZyB0aGUgb2Zmc2V0cyBmb3IgdGhlIHJvd3Mgb3IgY29sdW1ucyBwYXJzZWQuXG4gKlxuICogIyMjIyBOb3Rlc1xuICogVGhlIHBhcnNlcnMgYXJlIGJhc2VkIG9uIFtSRkMgNDE4MF0oaHR0cHM6Ly90b29scy5pZXRmLm9yZy9odG1sL3JmYzQxODApLlxuICovXG5leHBvcnQgdHlwZSBJUGFyc2VyID0gKG9wdGlvbnM6IElQYXJzZXIuSU9wdGlvbnMpID0+IElQYXJzZXIuSVJlc3VsdHM7XG5cbmV4cG9ydCBuYW1lc3BhY2UgSVBhcnNlciB7XG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyBmb3IgYSBwYXJzZXIuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgZGF0YSB0byBwYXJzZS5cbiAgICAgKi9cbiAgICBkYXRhOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIHJldHVybiBjb2x1bW4gb2Zmc2V0cyBpbiB0aGUgb2Zmc2V0cyBhcnJheS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBJZiBmYWxzZSwgdGhlIHJldHVybmVkIG9mZnNldHMgYXJyYXkgY29udGFpbnMganVzdCB0aGUgcm93IG9mZnNldHMuIElmXG4gICAgICogdHJ1ZSwgdGhlIHJldHVybmVkIG9mZnNldHMgYXJyYXkgY29udGFpbnMgYWxsIGNvbHVtbiBvZmZzZXRzIGZvciBlYWNoXG4gICAgICogY29sdW1uIGluIHRoZSByb3dzIChpLmUuLCBpdCBoYXMgbnJvd3MqbmNvbHMgZW50cmllcykuIEluZGl2aWR1YWwgcm93c1xuICAgICAqIHdpbGwgaGF2ZSBlbXB0eSBjb2x1bW5zIGFkZGVkIG9yIGV4dHJhIGNvbHVtbnMgbWVyZ2VkIGludG8gdGhlIGxhc3RcbiAgICAgKiBjb2x1bW4gaWYgdGhleSBkbyBub3QgaGF2ZSBleGFjdGx5IG5jb2xzIGNvbHVtbnMuXG4gICAgICovXG4gICAgY29sdW1uT2Zmc2V0czogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBkZWxpbWl0ZXIgdG8gdXNlLiBEZWZhdWx0cyB0byAnLCcuXG4gICAgICovXG4gICAgZGVsaW1pdGVyPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJvdyBkZWxpbWl0ZXIgdG8gdXNlLiBEZWZhdWx0cyB0byAnXFxyXFxuJy5cbiAgICAgKi9cbiAgICByb3dEZWxpbWl0ZXI/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcXVvdGUgY2hhcmFjdGVyIGZvciBxdW90aW5nIGZpZWxkcy4gRGVmYXVsdHMgdG8gdGhlIGRvdWJsZSBxdW90ZSAoXCIpLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIEFzIHNwZWNpZmllZCBpbiBbUkZDIDQxODBdKGh0dHBzOi8vdG9vbHMuaWV0Zi5vcmcvaHRtbC9yZmM0MTgwKSwgcXVvdGVzXG4gICAgICogYXJlIGVzY2FwZWQgaW4gYSBxdW90ZWQgZmllbGQgYnkgZG91YmxpbmcgdGhlbSAoZm9yIGV4YW1wbGUsIFwiYVwiXCJiXCIgaXMgdGhlIGZpZWxkXG4gICAgICogYVwiYikuXG4gICAgICovXG4gICAgcXVvdGU/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc3RhcnRpbmcgaW5kZXggaW4gdGhlIHN0cmluZyBmb3IgcHJvY2Vzc2luZy4gRGVmYXVsdHMgdG8gMC4gVGhpc1xuICAgICAqIGluZGV4IHNob3VsZCBiZSB0aGUgZmlyc3QgY2hhcmFjdGVyIG9mIGEgbmV3IHJvdy4gVGhpcyBtdXN0IGJlIGxlc3MgdGhhblxuICAgICAqIGRhdGEubGVuZ3RoLlxuICAgICAqL1xuICAgIHN0YXJ0SW5kZXg/OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBNYXhpbXVtIG51bWJlciBvZiByb3dzIHRvIHBhcnNlLlxuICAgICAqXG4gICAgICogSWYgdGhpcyBpcyBub3QgZ2l2ZW4sIHBhcnNpbmcgcHJvY2VlZHMgdG8gdGhlIGVuZCBvZiB0aGUgZGF0YS5cbiAgICAgKi9cbiAgICBtYXhSb3dzPzogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogTnVtYmVyIG9mIGNvbHVtbnMgaW4gZWFjaCByb3cgdG8gcGFyc2UuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogSWYgdGhpcyBpcyBub3QgZ2l2ZW4sIHRoZSBuY29scyBkZWZhdWx0cyB0byB0aGUgbnVtYmVyIG9mIGNvbHVtbnMgaW4gdGhlXG4gICAgICogZmlyc3Qgcm93LlxuICAgICAqL1xuICAgIG5jb2xzPzogbnVtYmVyO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSByZXN1bHRzIGZyb20gYSBwYXJzZXIuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElSZXN1bHRzIHtcbiAgICAvKipcbiAgICAgKiBUaGUgbnVtYmVyIG9mIHJvd3MgcGFyc2VkLlxuICAgICAqL1xuICAgIG5yb3dzOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbnVtYmVyIG9mIGNvbHVtbnMgcGFyc2VkLCBvciAwIGlmIG9ubHkgcm93IG9mZnNldHMgYXJlIHJldHVybmVkLlxuICAgICAqL1xuICAgIG5jb2xzOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgaW5kZXggb2Zmc2V0cyBpbnRvIHRoZSBkYXRhIHN0cmluZyBmb3IgdGhlIHJvd3Mgb3IgZGF0YSBpdGVtcy5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBJZiB0aGUgY29sdW1uT2Zmc2V0cyBhcmd1bWVudCB0byB0aGUgcGFyc2VyIGlzIGZhbHNlLCB0aGUgb2Zmc2V0cyBhcnJheVxuICAgICAqIHdpbGwgYmUgYW4gYXJyYXkgb2YgbGVuZ3RoIG5yb3dzLCB3aGVyZSBgb2Zmc2V0c1tyXWAgaXMgdGhlIGluZGV4IG9mIHRoZVxuICAgICAqIGZpcnN0IGNoYXJhY3RlciBvZiByb3cgci5cbiAgICAgKlxuICAgICAqIElmIHRoZSBjb2x1bW5PZmZzZXRzIGFyZ3VtZW50IHRvIHRoZSBwYXJzZXIgaXMgdHJ1ZSwgdGhlIG9mZnNldHMgYXJyYXlcbiAgICAgKiB3aWxsIGJlIGFuIGFycmF5IG9mIGxlbmd0aCBgbnJvd3MqbmNvbHNgLCB3aGVyZSBgb2Zmc2V0c1tyKm5jb2xzICsgY11gIGlzXG4gICAgICogdGhlIGluZGV4IG9mIHRoZSBmaXJzdCBjaGFyYWN0ZXIgb2YgdGhlIGl0ZW0gaW4gcm93IHIsIGNvbHVtbiBjLlxuICAgICAqL1xuICAgIG9mZnNldHM6IG51bWJlcltdO1xuICB9XG59XG5cbi8qKlxuICogUG9zc2libGUgcGFyc2VyIHN0YXRlcy5cbiAqL1xuZW51bSBTVEFURSB7XG4gIFFVT1RFRF9GSUVMRCxcbiAgUVVPVEVEX0ZJRUxEX1FVT1RFLFxuICBVTlFVT1RFRF9GSUVMRCxcbiAgTkVXX0ZJRUxELFxuICBORVdfUk9XXG59XG5cbi8qKlxuICogUG9zc2libGUgcm93IGRlbGltaXRlcnMgZm9yIHRoZSBwYXJzZXIuXG4gKi9cbmVudW0gUk9XX0RFTElNSVRFUiB7XG4gIENSLFxuICBDUkxGLFxuICBMRlxufVxuXG4vKipcbiAqIFBhcnNlIGRlbGltaXRlci1zZXBhcmF0ZWQgZGF0YS5cbiAqXG4gKiBAcGFyYW0gb3B0aW9uczogVGhlIHBhcnNlciBvcHRpb25zXG4gKiBAcmV0dXJucyBBbiBvYmplY3QgZ2l2aW5nIHRoZSBvZmZzZXRzIGZvciB0aGUgcm93cyBvciBjb2x1bW5zIHBhcnNlZC5cbiAqXG4gKiAjIyMjIE5vdGVzXG4gKiBUaGlzIGltcGxlbWVudGF0aW9uIGlzIGJhc2VkIG9uIFtSRkMgNDE4MF0oaHR0cHM6Ly90b29scy5pZXRmLm9yZy9odG1sL3JmYzQxODApLlxuICovXG5leHBvcnQgZnVuY3Rpb24gcGFyc2VEU1Yob3B0aW9uczogSVBhcnNlci5JT3B0aW9ucyk6IElQYXJzZXIuSVJlc3VsdHMge1xuICBjb25zdCB7XG4gICAgZGF0YSxcbiAgICBjb2x1bW5PZmZzZXRzLFxuICAgIGRlbGltaXRlciA9ICcsJyxcbiAgICBzdGFydEluZGV4ID0gMCxcbiAgICBtYXhSb3dzID0gMHhmZmZmZmZmZixcbiAgICByb3dEZWxpbWl0ZXIgPSAnXFxyXFxuJyxcbiAgICBxdW90ZSA9ICdcIidcbiAgfSA9IG9wdGlvbnM7XG5cbiAgLy8gbmNvbHMgd2lsbCBiZSBzZXQgYXV0b21hdGljYWxseSBpZiBpdCBpcyB1bmRlZmluZWQuXG4gIGxldCBuY29scyA9IG9wdGlvbnMubmNvbHM7XG5cbiAgLy8gVGhlIG51bWJlciBvZiByb3dzIHdlJ3ZlIGFscmVhZHkgcGFyc2VkLlxuICBsZXQgbnJvd3MgPSAwO1xuXG4gIC8vIFRoZSByb3cgb3IgY29sdW1uIG9mZnNldHMgd2UgcmV0dXJuLlxuICBjb25zdCBvZmZzZXRzID0gW107XG5cbiAgLy8gU2V0IHVwIHNvbWUgdXNlZnVsIGxvY2FsIHZhcmlhYmxlcy5cbiAgY29uc3QgQ0hfREVMSU1JVEVSID0gZGVsaW1pdGVyLmNoYXJDb2RlQXQoMCk7XG4gIGNvbnN0IENIX1FVT1RFID0gcXVvdGUuY2hhckNvZGVBdCgwKTtcbiAgY29uc3QgQ0hfTEYgPSAxMDsgLy8gXFxuXG4gIGNvbnN0IENIX0NSID0gMTM7IC8vIFxcclxuICBjb25zdCBlbmRJbmRleCA9IGRhdGEubGVuZ3RoO1xuICBjb25zdCB7XG4gICAgUVVPVEVEX0ZJRUxELFxuICAgIFFVT1RFRF9GSUVMRF9RVU9URSxcbiAgICBVTlFVT1RFRF9GSUVMRCxcbiAgICBORVdfRklFTEQsXG4gICAgTkVXX1JPV1xuICB9ID0gU1RBVEU7XG4gIGNvbnN0IHsgQ1IsIExGLCBDUkxGIH0gPSBST1dfREVMSU1JVEVSO1xuICBjb25zdCBbcm93RGVsaW1pdGVyQ29kZSwgcm93RGVsaW1pdGVyTGVuZ3RoXSA9XG4gICAgcm93RGVsaW1pdGVyID09PSAnXFxyXFxuJ1xuICAgICAgPyBbQ1JMRiwgMl1cbiAgICAgIDogcm93RGVsaW1pdGVyID09PSAnXFxyJ1xuICAgICAgPyBbQ1IsIDFdXG4gICAgICA6IFtMRiwgMV07XG5cbiAgLy8gQWx3YXlzIHN0YXJ0IG9mZiBhdCB0aGUgYmVnaW5uaW5nIG9mIGEgcm93LlxuICBsZXQgc3RhdGUgPSBORVdfUk9XO1xuXG4gIC8vIFNldCB1cCB0aGUgc3RhcnRpbmcgaW5kZXguXG4gIGxldCBpID0gc3RhcnRJbmRleDtcblxuICAvLyBXZSBpbml0aWFsaXplIHRvIDAganVzdCBpbiBjYXNlIHdlIGFyZSBhc2tlZCB0byBwYXJzZSBwYXN0IHRoZSBlbmQgb2YgdGhlXG4gIC8vIHN0cmluZy4gSW4gdGhhdCBjYXNlLCB3ZSB3YW50IHRoZSBudW1iZXIgb2YgY29sdW1ucyB0byBiZSAwLlxuICBsZXQgY29sID0gMDtcblxuICAvLyBEZWNsYXJlIHNvbWUgdXNlZnVsIHRlbXBvcmFyaWVzXG4gIGxldCBjaGFyO1xuXG4gIC8vIExvb3AgdGhyb3VnaCB0aGUgZGF0YSBzdHJpbmdcbiAgd2hpbGUgKGkgPCBlbmRJbmRleCkge1xuICAgIC8vIGkgaXMgdGhlIGluZGV4IG9mIGEgY2hhcmFjdGVyIGluIHRoZSBzdGF0ZS5cblxuICAgIC8vIElmIHdlIGp1c3QgaGl0IGEgbmV3IHJvdywgYW5kIHRoZXJlIGFyZSBzdGlsbCBjaGFyYWN0ZXJzIGxlZnQsIHB1c2ggYSBuZXdcbiAgICAvLyBvZmZzZXQgb24gYW5kIHJlc2V0IHRoZSBjb2x1bW4gY291bnRlci4gV2Ugd2FudCB0aGlzIGxvZ2ljIGF0IHRoZSB0b3Agb2ZcbiAgICAvLyB0aGUgd2hpbGUgbG9vcCByYXRoZXIgdGhhbiB0aGUgYm90dG9tIGJlY2F1c2Ugd2UgZG9uJ3Qgd2FudCBhIHRyYWlsaW5nXG4gICAgLy8gcm93IGRlbGltaXRlciBhdCB0aGUgZW5kIG9mIHRoZSBkYXRhIHRvIHRyaWdnZXIgYSBuZXcgcm93IG9mZnNldC5cbiAgICBpZiAoc3RhdGUgPT09IE5FV19ST1cpIHtcbiAgICAgIC8vIFN0YXJ0IGEgbmV3IHJvdyBhbmQgcmVzZXQgdGhlIGNvbHVtbiBjb3VudGVyLlxuICAgICAgb2Zmc2V0cy5wdXNoKGkpO1xuICAgICAgY29sID0gMTtcbiAgICB9XG5cbiAgICAvLyBCZWxvdywgd2UgaGFuZGxlIHRoaXMgY2hhcmFjdGVyLCBtb2RpZnkgdGhlIHBhcnNlciBzdGF0ZSBhbmQgaW5jcmVtZW50IHRoZSBpbmRleCB0byBiZSBjb25zaXN0ZW50LlxuXG4gICAgLy8gR2V0IHRoZSBpbnRlZ2VyIGNvZGUgZm9yIHRoZSBjdXJyZW50IGNoYXJhY3Rlciwgc28gdGhlIGNvbXBhcmlzb25zIGJlbG93XG4gICAgLy8gYXJlIGZhc3Rlci5cbiAgICBjaGFyID0gZGF0YS5jaGFyQ29kZUF0KGkpO1xuXG4gICAgLy8gVXBkYXRlIHRoZSBwYXJzZXIgc3RhdGUuIFRoaXMgc3dpdGNoIHN0YXRlbWVudCBpcyByZXNwb25zaWJsZSBmb3JcbiAgICAvLyB1cGRhdGluZyB0aGUgc3RhdGUgdG8gYmUgY29uc2lzdGVudCB3aXRoIHRoZSBpbmRleCBpKzEgKHdlIGluY3JlbWVudCBpXG4gICAgLy8gYWZ0ZXIgdGhlIHN3aXRjaCBzdGF0ZW1lbnQpLiBJbiBzb21lIHNpdHVhdGlvbnMsIHdlIG1heSBpbmNyZW1lbnQgaVxuICAgIC8vIGluc2lkZSB0aGlzIGxvb3AgdG8gc2tpcCBvdmVyIGluZGljZXMgYXMgYSBzaG9ydGN1dC5cbiAgICBzd2l0Y2ggKHN0YXRlKSB7XG4gICAgICAvLyBBdCB0aGUgYmVnaW5uaW5nIG9mIGEgcm93IG9yIGZpZWxkLCB3ZSBjYW4gaGF2ZSBhIHF1b3RlLCByb3cgZGVsaW1pdGVyLCBvciBmaWVsZCBkZWxpbWl0ZXIuXG4gICAgICBjYXNlIE5FV19ST1c6XG4gICAgICBjYXNlIE5FV19GSUVMRDpcbiAgICAgICAgc3dpdGNoIChjaGFyKSB7XG4gICAgICAgICAgLy8gSWYgd2UgaGF2ZSBhIHF1b3RlLCB3ZSBhcmUgc3RhcnRpbmcgYW4gZXNjYXBlZCBmaWVsZC5cbiAgICAgICAgICBjYXNlIENIX1FVT1RFOlxuICAgICAgICAgICAgc3RhdGUgPSBRVU9URURfRklFTEQ7XG4gICAgICAgICAgICBicmVhaztcblxuICAgICAgICAgIC8vIEEgZmllbGQgZGVsaW1pdGVyIG1lYW5zIHdlIGFyZSBzdGFydGluZyBhIG5ldyBmaWVsZC5cbiAgICAgICAgICBjYXNlIENIX0RFTElNSVRFUjpcbiAgICAgICAgICAgIHN0YXRlID0gTkVXX0ZJRUxEO1xuICAgICAgICAgICAgYnJlYWs7XG5cbiAgICAgICAgICAvLyBBIHJvdyBkZWxpbWl0ZXIgbWVhbnMgd2UgYXJlIHN0YXJ0aW5nIGEgbmV3IHJvdy5cbiAgICAgICAgICBjYXNlIENIX0NSOlxuICAgICAgICAgICAgaWYgKHJvd0RlbGltaXRlckNvZGUgPT09IENSKSB7XG4gICAgICAgICAgICAgIHN0YXRlID0gTkVXX1JPVztcbiAgICAgICAgICAgIH0gZWxzZSBpZiAoXG4gICAgICAgICAgICAgIHJvd0RlbGltaXRlckNvZGUgPT09IENSTEYgJiZcbiAgICAgICAgICAgICAgZGF0YS5jaGFyQ29kZUF0KGkgKyAxKSA9PT0gQ0hfTEZcbiAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAvLyBJZiB3ZSBzZWUgYW4gZXhwZWN0ZWQgXFxyXFxuLCB0aGVuIGluY3JlbWVudCB0byB0aGUgZW5kIG9mIHRoZSBkZWxpbWl0ZXIuXG4gICAgICAgICAgICAgIGkrKztcbiAgICAgICAgICAgICAgc3RhdGUgPSBORVdfUk9XO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgdGhyb3cgYHN0cmluZyBpbmRleCAke2l9IChpbiByb3cgJHtucm93c30sIGNvbHVtbiAke2NvbH0pOiBjYXJyaWFnZSByZXR1cm4gZm91bmQsIGJ1dCBub3QgYXMgcGFydCBvZiBhIHJvdyBkZWxpbWl0ZXIgQyAke2RhdGEuY2hhckNvZGVBdChcbiAgICAgICAgICAgICAgICBpICsgMVxuICAgICAgICAgICAgICApfWA7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBicmVhaztcbiAgICAgICAgICBjYXNlIENIX0xGOlxuICAgICAgICAgICAgaWYgKHJvd0RlbGltaXRlckNvZGUgPT09IExGKSB7XG4gICAgICAgICAgICAgIHN0YXRlID0gTkVXX1JPVztcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgIHRocm93IGBzdHJpbmcgaW5kZXggJHtpfSAoaW4gcm93ICR7bnJvd3N9LCBjb2x1bW4gJHtjb2x9KTogbGluZSBmZWVkIGZvdW5kLCBidXQgcm93IGRlbGltaXRlciBzdGFydHMgd2l0aCBhIGNhcnJpYWdlIHJldHVybmA7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBicmVhaztcblxuICAgICAgICAgIC8vIE90aGVyd2lzZSwgd2UgYXJlIHN0YXJ0aW5nIGFuIHVucXVvdGVkIGZpZWxkLlxuICAgICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgICBzdGF0ZSA9IFVOUVVPVEVEX0ZJRUxEO1xuICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG5cbiAgICAgIC8vIFdlIGFyZSBpbiBhIHF1b3RlZCBmaWVsZC5cbiAgICAgIGNhc2UgUVVPVEVEX0ZJRUxEOlxuICAgICAgICAvLyBTa2lwIGFoZWFkIHVudGlsIHdlIHNlZSBhbm90aGVyIHF1b3RlLCB3aGljaCBlaXRoZXIgZW5kcyB0aGUgcXVvdGVkXG4gICAgICAgIC8vIGZpZWxkIG9yIHN0YXJ0cyBhbiBlc2NhcGVkIHF1b3RlLlxuICAgICAgICBpID0gZGF0YS5pbmRleE9mKHF1b3RlLCBpKTtcbiAgICAgICAgaWYgKGkgPCAwKSB7XG4gICAgICAgICAgdGhyb3cgYHN0cmluZyBpbmRleCAke2l9IChpbiByb3cgJHtucm93c30sIGNvbHVtbiAke2NvbH0pOiBtaXNtYXRjaGVkIHF1b3RlYDtcbiAgICAgICAgfVxuICAgICAgICBzdGF0ZSA9IFFVT1RFRF9GSUVMRF9RVU9URTtcbiAgICAgICAgYnJlYWs7XG5cbiAgICAgIC8vIFdlIGp1c3Qgc2F3IGEgcXVvdGUgaW4gYSBxdW90ZWQgZmllbGQuIFRoaXMgY291bGQgYmUgdGhlIGVuZCBvZiB0aGVcbiAgICAgIC8vIGZpZWxkLCBvciBpdCBjb3VsZCBiZSBhIHJlcGVhdGVkIHF1b3RlIChpLmUuLCBhbiBlc2NhcGVkIHF1b3RlIGFjY29yZGluZ1xuICAgICAgLy8gdG8gUkZDIDQxODApLlxuICAgICAgY2FzZSBRVU9URURfRklFTERfUVVPVEU6XG4gICAgICAgIHN3aXRjaCAoY2hhcikge1xuICAgICAgICAgIC8vIEFub3RoZXIgcXVvdGUgbWVhbnMgd2UganVzdCBzYXcgYW4gZXNjYXBlZCBxdW90ZSwgc28gd2UgYXJlIHN0aWxsIGluXG4gICAgICAgICAgLy8gdGhlIHF1b3RlZCBmaWVsZC5cbiAgICAgICAgICBjYXNlIENIX1FVT1RFOlxuICAgICAgICAgICAgc3RhdGUgPSBRVU9URURfRklFTEQ7XG4gICAgICAgICAgICBicmVhaztcblxuICAgICAgICAgIC8vIEEgZmllbGQgb3Igcm93IGRlbGltaXRlciBtZWFucyB0aGUgcXVvdGVkIGZpZWxkIGp1c3QgZW5kZWQgYW5kIHdlIGFyZVxuICAgICAgICAgIC8vIGdvaW5nIGludG8gYSBuZXcgZmllbGQgb3IgbmV3IHJvdy5cbiAgICAgICAgICBjYXNlIENIX0RFTElNSVRFUjpcbiAgICAgICAgICAgIHN0YXRlID0gTkVXX0ZJRUxEO1xuICAgICAgICAgICAgYnJlYWs7XG5cbiAgICAgICAgICAvLyBBIHJvdyBkZWxpbWl0ZXIgbWVhbnMgd2UgYXJlIHN0YXJ0aW5nIGEgbmV3IHJvdyBpbiB0aGUgbmV4dCBpbmRleC5cbiAgICAgICAgICBjYXNlIENIX0NSOlxuICAgICAgICAgICAgaWYgKHJvd0RlbGltaXRlckNvZGUgPT09IENSKSB7XG4gICAgICAgICAgICAgIHN0YXRlID0gTkVXX1JPVztcbiAgICAgICAgICAgIH0gZWxzZSBpZiAoXG4gICAgICAgICAgICAgIHJvd0RlbGltaXRlckNvZGUgPT09IENSTEYgJiZcbiAgICAgICAgICAgICAgZGF0YS5jaGFyQ29kZUF0KGkgKyAxKSA9PT0gQ0hfTEZcbiAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAvLyBJZiB3ZSBzZWUgYW4gZXhwZWN0ZWQgXFxyXFxuLCB0aGVuIGluY3JlbWVudCB0byB0aGUgZW5kIG9mIHRoZSBkZWxpbWl0ZXIuXG4gICAgICAgICAgICAgIGkrKztcbiAgICAgICAgICAgICAgc3RhdGUgPSBORVdfUk9XO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgdGhyb3cgYHN0cmluZyBpbmRleCAke2l9IChpbiByb3cgJHtucm93c30sIGNvbHVtbiAke2NvbH0pOiBjYXJyaWFnZSByZXR1cm4gZm91bmQsIGJ1dCBub3QgYXMgcGFydCBvZiBhIHJvdyBkZWxpbWl0ZXIgQyAke2RhdGEuY2hhckNvZGVBdChcbiAgICAgICAgICAgICAgICBpICsgMVxuICAgICAgICAgICAgICApfWA7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBicmVhaztcbiAgICAgICAgICBjYXNlIENIX0xGOlxuICAgICAgICAgICAgaWYgKHJvd0RlbGltaXRlckNvZGUgPT09IExGKSB7XG4gICAgICAgICAgICAgIHN0YXRlID0gTkVXX1JPVztcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgIHRocm93IGBzdHJpbmcgaW5kZXggJHtpfSAoaW4gcm93ICR7bnJvd3N9LCBjb2x1bW4gJHtjb2x9KTogbGluZSBmZWVkIGZvdW5kLCBidXQgcm93IGRlbGltaXRlciBzdGFydHMgd2l0aCBhIGNhcnJpYWdlIHJldHVybmA7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBicmVhaztcblxuICAgICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgICB0aHJvdyBgc3RyaW5nIGluZGV4ICR7aX0gKGluIHJvdyAke25yb3dzfSwgY29sdW1uICR7Y29sfSk6IHF1b3RlIGluIGVzY2FwZWQgZmllbGQgbm90IGZvbGxvd2VkIGJ5IHF1b3RlLCBkZWxpbWl0ZXIsIG9yIHJvdyBkZWxpbWl0ZXJgO1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuXG4gICAgICAvLyBXZSBhcmUgaW4gYW4gdW5xdW90ZWQgZmllbGQsIHNvIHRoZSBvbmx5IHRoaW5nIHdlIGxvb2sgZm9yIGlzIHRoZSBuZXh0XG4gICAgICAvLyByb3cgb3IgZmllbGQgZGVsaW1pdGVyLlxuICAgICAgY2FzZSBVTlFVT1RFRF9GSUVMRDpcbiAgICAgICAgLy8gU2tpcCBhaGVhZCB0byBlaXRoZXIgdGhlIG5leHQgZmllbGQgZGVsaW1pdGVyIG9yIHBvc3NpYmxlIHN0YXJ0IG9mIGFcbiAgICAgICAgLy8gcm93IGRlbGltaXRlciAoQ1Igb3IgTEYpLlxuICAgICAgICB3aGlsZSAoaSA8IGVuZEluZGV4KSB7XG4gICAgICAgICAgY2hhciA9IGRhdGEuY2hhckNvZGVBdChpKTtcbiAgICAgICAgICBpZiAoY2hhciA9PT0gQ0hfREVMSU1JVEVSIHx8IGNoYXIgPT09IENIX0xGIHx8IGNoYXIgPT09IENIX0NSKSB7XG4gICAgICAgICAgICBicmVhaztcbiAgICAgICAgICB9XG4gICAgICAgICAgaSsrO1xuICAgICAgICB9XG5cbiAgICAgICAgLy8gUHJvY2VzcyB0aGUgY2hhcmFjdGVyIHdlJ3JlIHNlZWluZyBpbiBhbiB1bnF1b3RlZCBmaWVsZC5cbiAgICAgICAgc3dpdGNoIChjaGFyKSB7XG4gICAgICAgICAgLy8gQSBmaWVsZCBkZWxpbWl0ZXIgbWVhbnMgd2UgYXJlIHN0YXJ0aW5nIGEgbmV3IGZpZWxkLlxuICAgICAgICAgIGNhc2UgQ0hfREVMSU1JVEVSOlxuICAgICAgICAgICAgc3RhdGUgPSBORVdfRklFTEQ7XG4gICAgICAgICAgICBicmVhaztcblxuICAgICAgICAgIC8vIEEgcm93IGRlbGltaXRlciBtZWFucyB3ZSBhcmUgc3RhcnRpbmcgYSBuZXcgcm93IGluIHRoZSBuZXh0IGluZGV4LlxuICAgICAgICAgIGNhc2UgQ0hfQ1I6XG4gICAgICAgICAgICBpZiAocm93RGVsaW1pdGVyQ29kZSA9PT0gQ1IpIHtcbiAgICAgICAgICAgICAgc3RhdGUgPSBORVdfUk9XO1xuICAgICAgICAgICAgfSBlbHNlIGlmIChcbiAgICAgICAgICAgICAgcm93RGVsaW1pdGVyQ29kZSA9PT0gQ1JMRiAmJlxuICAgICAgICAgICAgICBkYXRhLmNoYXJDb2RlQXQoaSArIDEpID09PSBDSF9MRlxuICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgIC8vIElmIHdlIHNlZSBhbiBleHBlY3RlZCBcXHJcXG4sIHRoZW4gaW5jcmVtZW50IHRvIHRoZSBlbmQgb2YgdGhlIGRlbGltaXRlci5cbiAgICAgICAgICAgICAgaSsrO1xuICAgICAgICAgICAgICBzdGF0ZSA9IE5FV19ST1c7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICB0aHJvdyBgc3RyaW5nIGluZGV4ICR7aX0gKGluIHJvdyAke25yb3dzfSwgY29sdW1uICR7Y29sfSk6IGNhcnJpYWdlIHJldHVybiBmb3VuZCwgYnV0IG5vdCBhcyBwYXJ0IG9mIGEgcm93IGRlbGltaXRlciBDICR7ZGF0YS5jaGFyQ29kZUF0KFxuICAgICAgICAgICAgICAgIGkgKyAxXG4gICAgICAgICAgICAgICl9YDtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgIGNhc2UgQ0hfTEY6XG4gICAgICAgICAgICBpZiAocm93RGVsaW1pdGVyQ29kZSA9PT0gTEYpIHtcbiAgICAgICAgICAgICAgc3RhdGUgPSBORVdfUk9XO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgdGhyb3cgYHN0cmluZyBpbmRleCAke2l9IChpbiByb3cgJHtucm93c30sIGNvbHVtbiAke2NvbH0pOiBsaW5lIGZlZWQgZm91bmQsIGJ1dCByb3cgZGVsaW1pdGVyIHN0YXJ0cyB3aXRoIGEgY2FycmlhZ2UgcmV0dXJuYDtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGJyZWFrO1xuXG4gICAgICAgICAgLy8gT3RoZXJ3aXNlLCB3ZSBjb250aW51ZSBvbiBpbiB0aGUgdW5xdW90ZWQgZmllbGQuXG4gICAgICAgICAgZGVmYXVsdDpcbiAgICAgICAgICAgIGNvbnRpbnVlO1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuXG4gICAgICAvLyBXZSBzaG91bGQgbmV2ZXIgcmVhY2ggdGhpcyBwb2ludCBzaW5jZSB0aGUgcGFyc2VyIHN0YXRlIGlzIGhhbmRsZWQgYWJvdmUsXG4gICAgICAvLyBzbyB0aHJvdyBhbiBlcnJvciBpZiB3ZSBkby5cbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIHRocm93IGBzdHJpbmcgaW5kZXggJHtpfSAoaW4gcm93ICR7bnJvd3N9LCBjb2x1bW4gJHtjb2x9KTogc3RhdGUgbm90IHJlY29nbml6ZWRgO1xuICAgIH1cblxuICAgIC8vIEluY3JlbWVudCBpIHRvIHRoZSBuZXh0IGNoYXJhY3RlciBpbmRleFxuICAgIGkrKztcblxuICAgIC8vIFVwZGF0ZSByZXR1cm4gdmFsdWVzIGJhc2VkIG9uIHN0YXRlLlxuICAgIHN3aXRjaCAoc3RhdGUpIHtcbiAgICAgIGNhc2UgTkVXX1JPVzpcbiAgICAgICAgbnJvd3MrKztcblxuICAgICAgICAvLyBJZiBuY29scyBpcyB1bmRlZmluZWQsIHNldCBpdCB0byB0aGUgbnVtYmVyIG9mIGNvbHVtbnMgaW4gdGhpcyByb3cgKGZpcnN0IHJvdyBpbXBsaWVkKS5cbiAgICAgICAgaWYgKG5jb2xzID09PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICBpZiAobnJvd3MgIT09IDEpIHtcbiAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcignRXJyb3IgcGFyc2luZyBkZWZhdWx0IG51bWJlciBvZiBjb2x1bW5zJyk7XG4gICAgICAgICAgfVxuICAgICAgICAgIG5jb2xzID0gY29sO1xuICAgICAgICB9XG5cbiAgICAgICAgLy8gUGFkIG9yIHRydW5jYXRlIHRoZSBjb2x1bW4gb2Zmc2V0cyBpbiB0aGUgcHJldmlvdXMgcm93IGlmIHdlIGFyZVxuICAgICAgICAvLyByZXR1cm5pbmcgdGhlbS5cbiAgICAgICAgaWYgKGNvbHVtbk9mZnNldHMgPT09IHRydWUpIHtcbiAgICAgICAgICBpZiAoY29sIDwgbmNvbHMpIHtcbiAgICAgICAgICAgIC8vIFdlIGRpZG4ndCBoYXZlIGVub3VnaCBjb2x1bW5zLCBzbyBhZGQgc29tZSBtb3JlIGNvbHVtbiBvZmZzZXRzIHRoYXRcbiAgICAgICAgICAgIC8vIHBvaW50IHRvIGp1c3QgYmVmb3JlIHRoZSByb3cgZGVsaW1pdGVyIHdlIGp1c3Qgc2F3LlxuICAgICAgICAgICAgZm9yICg7IGNvbCA8IG5jb2xzOyBjb2wrKykge1xuICAgICAgICAgICAgICBvZmZzZXRzLnB1c2goaSAtIHJvd0RlbGltaXRlckxlbmd0aCk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSBlbHNlIGlmIChjb2wgPiBuY29scykge1xuICAgICAgICAgICAgLy8gV2UgaGFkIHRvbyBtYW55IGNvbHVtbnMsIHNvIHRydW5jYXRlIHRoZW0uXG4gICAgICAgICAgICBvZmZzZXRzLmxlbmd0aCA9IG9mZnNldHMubGVuZ3RoIC0gKGNvbCAtIG5jb2xzKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cblxuICAgICAgICAvLyBTaG9ydGN1dCByZXR1cm4gaWYgbnJvd3MgcmVhY2hlcyB0aGUgbWF4aW11bSByb3dzIHdlIGFyZSB0byBwYXJzZS5cbiAgICAgICAgaWYgKG5yb3dzID09PSBtYXhSb3dzKSB7XG4gICAgICAgICAgcmV0dXJuIHsgbnJvd3MsIG5jb2xzOiBjb2x1bW5PZmZzZXRzID8gbmNvbHMgOiAwLCBvZmZzZXRzIH07XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG5cbiAgICAgIGNhc2UgTkVXX0ZJRUxEOlxuICAgICAgICAvLyBJZiB3ZSBhcmUgcmV0dXJuaW5nIGNvbHVtbiBvZmZzZXRzLCBsb2cgdGhlIGN1cnJlbnQgaW5kZXguXG4gICAgICAgIGlmIChjb2x1bW5PZmZzZXRzID09PSB0cnVlKSB7XG4gICAgICAgICAgb2Zmc2V0cy5wdXNoKGkpO1xuICAgICAgICB9XG5cbiAgICAgICAgLy8gVXBkYXRlIHRoZSBjb2x1bW4gY291bnRlci5cbiAgICAgICAgY29sKys7XG4gICAgICAgIGJyZWFrO1xuXG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvLyBJZiB3ZSBmaW5pc2hlZCBwYXJzaW5nIGFuZCB3ZSBhcmUgKm5vdCogaW4gdGhlIE5FV19ST1cgc3RhdGUsIHRoZW4gZG8gdGhlXG4gIC8vIGNvbHVtbiBwYWRkaW5nL3RydW5jYXRpb24gZm9yIHRoZSBsYXN0IHJvdy4gQWxzbyBtYWtlIHN1cmUgbmNvbHMgaXNcbiAgLy8gZGVmaW5lZC5cbiAgaWYgKHN0YXRlICE9PSBORVdfUk9XKSB7XG4gICAgbnJvd3MrKztcbiAgICBpZiAoY29sdW1uT2Zmc2V0cyA9PT0gdHJ1ZSkge1xuICAgICAgLy8gSWYgbmNvbHMgaXMgKnN0aWxsKiB1bmRlZmluZWQsIHRoZW4gd2Ugb25seSBwYXJzZWQgb25lIHJvdyBhbmQgZGlkbid0XG4gICAgICAvLyBoYXZlIGEgbmV3bGluZSwgc28gc2V0IGl0IHRvIHRoZSBudW1iZXIgb2YgY29sdW1ucyB3ZSBmb3VuZC5cbiAgICAgIGlmIChuY29scyA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICAgIG5jb2xzID0gY29sO1xuICAgICAgfVxuXG4gICAgICBpZiAoY29sIDwgbmNvbHMpIHtcbiAgICAgICAgLy8gV2UgZGlkbid0IGhhdmUgZW5vdWdoIGNvbHVtbnMsIHNvIGFkZCBzb21lIG1vcmUgY29sdW1uIG9mZnNldHMgdGhhdFxuICAgICAgICAvLyBwb2ludCB0byBqdXN0IGJlZm9yZSB0aGUgcm93IGRlbGltaXRlciB3ZSBqdXN0IHNhdy5cbiAgICAgICAgZm9yICg7IGNvbCA8IG5jb2xzOyBjb2wrKykge1xuICAgICAgICAgIG9mZnNldHMucHVzaChpIC0gKHJvd0RlbGltaXRlckxlbmd0aCAtIDEpKTtcbiAgICAgICAgfVxuICAgICAgfSBlbHNlIGlmIChjb2wgPiBuY29scykge1xuICAgICAgICAvLyBXZSBoYWQgdG9vIG1hbnkgY29sdW1ucywgc28gdHJ1bmNhdGUgdGhlbS5cbiAgICAgICAgb2Zmc2V0cy5sZW5ndGggPSBvZmZzZXRzLmxlbmd0aCAtIChjb2wgLSBuY29scyk7XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgcmV0dXJuIHsgbnJvd3MsIG5jb2xzOiBjb2x1bW5PZmZzZXRzID8gbmNvbHMgPz8gMCA6IDAsIG9mZnNldHMgfTtcbn1cblxuLyoqXG4gKiBQYXJzZSBkZWxpbWl0ZXItc2VwYXJhdGVkIGRhdGEgd2hlcmUgbm8gZGVsaW1pdGVyIGlzIHF1b3RlZC5cbiAqXG4gKiBAcGFyYW0gb3B0aW9uczogVGhlIHBhcnNlciBvcHRpb25zXG4gKiBAcmV0dXJucyBBbiBvYmplY3QgZ2l2aW5nIHRoZSBvZmZzZXRzIGZvciB0aGUgcm93cyBvciBjb2x1bW5zIHBhcnNlZC5cbiAqXG4gKiAjIyMjIE5vdGVzXG4gKiBUaGlzIGZ1bmN0aW9uIGlzIGFuIG9wdGltaXplZCBwYXJzZXIgZm9yIGNhc2VzIHdoZXJlIHRoZXJlIGFyZSBubyBmaWVsZCBvclxuICogcm93IGRlbGltaXRlcnMgaW4gcXVvdGVzLiBOb3RlIHRoYXQgdGhlIGRhdGEgY2FuIGhhdmUgcXVvdGVzLCBidXQgdGhleSBhcmVcbiAqIG5vdCBpbnRlcnByZXRlZCBpbiBhbnkgc3BlY2lhbCB3YXkuIFRoaXMgaW1wbGVtZW50YXRpb24gaXMgYmFzZWQgb24gW1JGQ1xuICogNDE4MF0oaHR0cHM6Ly90b29scy5pZXRmLm9yZy9odG1sL3JmYzQxODApLCBidXQgZGlzcmVnYXJkcyBxdW90ZXMuXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBwYXJzZURTVk5vUXVvdGVzKG9wdGlvbnM6IElQYXJzZXIuSU9wdGlvbnMpOiBJUGFyc2VyLklSZXN1bHRzIHtcbiAgLy8gU2V0IG9wdGlvbiBkZWZhdWx0cy5cbiAgY29uc3Qge1xuICAgIGRhdGEsXG4gICAgY29sdW1uT2Zmc2V0cyxcbiAgICBkZWxpbWl0ZXIgPSAnLCcsXG4gICAgcm93RGVsaW1pdGVyID0gJ1xcclxcbicsXG4gICAgc3RhcnRJbmRleCA9IDAsXG4gICAgbWF4Um93cyA9IDB4ZmZmZmZmZmZcbiAgfSA9IG9wdGlvbnM7XG5cbiAgLy8gbmNvbHMgd2lsbCBiZSBzZXQgYXV0b21hdGljYWxseSBpZiBpdCBpcyB1bmRlZmluZWQuXG4gIGxldCBuY29scyA9IG9wdGlvbnMubmNvbHM7XG5cbiAgLy8gU2V0IHVwIG91ciByZXR1cm4gdmFyaWFibGVzLlxuICBjb25zdCBvZmZzZXRzOiBudW1iZXJbXSA9IFtdO1xuICBsZXQgbnJvd3MgPSAwO1xuXG4gIC8vIFNldCB1cCB2YXJpb3VzIHN0YXRlIHZhcmlhYmxlcy5cbiAgY29uc3Qgcm93RGVsaW1pdGVyTGVuZ3RoID0gcm93RGVsaW1pdGVyLmxlbmd0aDtcbiAgbGV0IGN1cnJSb3cgPSBzdGFydEluZGV4O1xuICBjb25zdCBsZW4gPSBkYXRhLmxlbmd0aDtcbiAgbGV0IG5leHRSb3c6IG51bWJlcjtcbiAgbGV0IGNvbDogbnVtYmVyO1xuICBsZXQgcm93U3RyaW5nOiBzdHJpbmc7XG4gIGxldCBjb2xJbmRleDogbnVtYmVyO1xuXG4gIC8vIFRoZSBlbmQgb2YgdGhlIGN1cnJlbnQgcm93LlxuICBsZXQgcm93RW5kOiBudW1iZXI7XG5cbiAgLy8gU3RhcnQgcGFyc2luZyBhdCB0aGUgc3RhcnQgaW5kZXguXG4gIG5leHRSb3cgPSBzdGFydEluZGV4O1xuXG4gIC8vIExvb3AgdGhyb3VnaCByb3dzIHVudGlsIHdlIHJ1biBvdXQgb2YgZGF0YSBvciB3ZSd2ZSByZWFjaGVkIG1heFJvd3MuXG4gIHdoaWxlIChuZXh0Um93ICE9PSAtMSAmJiBucm93cyA8IG1heFJvd3MgJiYgY3VyclJvdyA8IGxlbikge1xuICAgIC8vIFN0b3JlIHRoZSBvZmZzZXQgZm9yIHRoZSBiZWdpbm5pbmcgb2YgdGhlIHJvdyBhbmQgaW5jcmVtZW50IHRoZSByb3dzLlxuICAgIG9mZnNldHMucHVzaChjdXJyUm93KTtcbiAgICBucm93cysrO1xuXG4gICAgLy8gRmluZCB0aGUgbmV4dCByb3cgZGVsaW1pdGVyLlxuICAgIG5leHRSb3cgPSBkYXRhLmluZGV4T2Yocm93RGVsaW1pdGVyLCBjdXJyUm93KTtcblxuICAgIC8vIElmIHRoZSBuZXh0IHJvdyBkZWxpbWl0ZXIgaXMgbm90IGZvdW5kLCBzZXQgdGhlIGVuZCBvZiB0aGUgcm93IHRvIHRoZVxuICAgIC8vIGVuZCBvZiB0aGUgZGF0YSBzdHJpbmcuXG4gICAgcm93RW5kID0gbmV4dFJvdyA9PT0gLTEgPyBsZW4gOiBuZXh0Um93O1xuXG4gICAgLy8gSWYgd2UgYXJlIHJldHVybmluZyBjb2x1bW4gb2Zmc2V0cywgcHVzaCB0aGVtIG9udG8gdGhlIGFycmF5LlxuICAgIGlmIChjb2x1bW5PZmZzZXRzID09PSB0cnVlKSB7XG4gICAgICAvLyBGaW5kIHRoZSBuZXh0IGZpZWxkIGRlbGltaXRlci4gV2Ugc2xpY2UgdGhlIGN1cnJlbnQgcm93IG91dCBzbyB0aGF0XG4gICAgICAvLyB0aGUgaW5kZXhPZiB3aWxsIHN0b3AgYXQgdGhlIGVuZCBvZiB0aGUgcm93LiBJdCBtYXkgcG9zc2libHkgYmUgZmFzdGVyXG4gICAgICAvLyB0byBqdXN0IHVzZSBhIGxvb3AgdG8gY2hlY2sgZWFjaCBjaGFyYWN0ZXIuXG4gICAgICBjb2wgPSAxO1xuICAgICAgcm93U3RyaW5nID0gZGF0YS5zbGljZShjdXJyUm93LCByb3dFbmQpO1xuICAgICAgY29sSW5kZXggPSByb3dTdHJpbmcuaW5kZXhPZihkZWxpbWl0ZXIpO1xuXG4gICAgICBpZiAobmNvbHMgPT09IHVuZGVmaW5lZCkge1xuICAgICAgICAvLyBJZiB3ZSBkb24ndCBrbm93IGhvdyBtYW55IGNvbHVtbnMgd2UgbmVlZCwgbG9vcCB0aHJvdWdoIGFuZCBmaW5kIGFsbFxuICAgICAgICAvLyBvZiB0aGUgZmllbGQgZGVsaW1pdGVycyBpbiB0aGlzIHJvdy5cbiAgICAgICAgd2hpbGUgKGNvbEluZGV4ICE9PSAtMSkge1xuICAgICAgICAgIG9mZnNldHMucHVzaChjdXJyUm93ICsgY29sSW5kZXggKyAxKTtcbiAgICAgICAgICBjb2wrKztcbiAgICAgICAgICBjb2xJbmRleCA9IHJvd1N0cmluZy5pbmRleE9mKGRlbGltaXRlciwgY29sSW5kZXggKyAxKTtcbiAgICAgICAgfVxuXG4gICAgICAgIC8vIFNldCBuY29scyB0byB0aGUgbnVtYmVyIG9mIGZpZWxkcyB3ZSBmb3VuZC5cbiAgICAgICAgbmNvbHMgPSBjb2w7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICAvLyBJZiB3ZSBrbm93IHRoZSBudW1iZXIgb2YgY29sdW1ucyB3ZSBleHBlY3QsIGZpbmQgdGhlIGZpZWxkIGRlbGltaXRlcnNcbiAgICAgICAgLy8gdXAgdG8gdGhhdCBtYW55IGNvbHVtbnMuXG4gICAgICAgIHdoaWxlIChjb2xJbmRleCAhPT0gLTEgJiYgY29sIDwgbmNvbHMpIHtcbiAgICAgICAgICBvZmZzZXRzLnB1c2goY3VyclJvdyArIGNvbEluZGV4ICsgMSk7XG4gICAgICAgICAgY29sKys7XG4gICAgICAgICAgY29sSW5kZXggPSByb3dTdHJpbmcuaW5kZXhPZihkZWxpbWl0ZXIsIGNvbEluZGV4ICsgMSk7XG4gICAgICAgIH1cblxuICAgICAgICAvLyBJZiB3ZSBkaWRuJ3QgcmVhY2ggdGhlIG51bWJlciBvZiBjb2x1bW5zIHdlIGV4cGVjdGVkLCBwYWQgdGhlIG9mZnNldHNcbiAgICAgICAgLy8gd2l0aCB0aGUgb2Zmc2V0IGp1c3QgYmVmb3JlIHRoZSByb3cgZGVsaW1pdGVyLlxuICAgICAgICB3aGlsZSAoY29sIDwgbmNvbHMpIHtcbiAgICAgICAgICBvZmZzZXRzLnB1c2gocm93RW5kKTtcbiAgICAgICAgICBjb2wrKztcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cblxuICAgIC8vIFNraXAgcGFzdCB0aGUgcm93IGRlbGltaXRlciBhdCB0aGUgZW5kIG9mIHRoZSByb3cuXG4gICAgY3VyclJvdyA9IHJvd0VuZCArIHJvd0RlbGltaXRlckxlbmd0aDtcbiAgfVxuXG4gIHJldHVybiB7IG5yb3dzLCBuY29sczogY29sdW1uT2Zmc2V0cyA/IG5jb2xzID8/IDAgOiAwLCBvZmZzZXRzIH07XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFN0eWxpbmcgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgbnVsbFRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBlYWNoIH0gZnJvbSAnQGx1bWluby9hbGdvcml0aG0nO1xuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gYSBjc3YgdG9vbGJhciB3aWRnZXQuXG4gKi9cbmNvbnN0IENTVl9ERUxJTUlURVJfQ0xBU1MgPSAnanAtQ1NWRGVsaW1pdGVyJztcblxuY29uc3QgQ1NWX0RFTElNSVRFUl9MQUJFTF9DTEFTUyA9ICdqcC1DU1ZEZWxpbWl0ZXItbGFiZWwnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGEgY3N2IHRvb2xiYXIncyBkcm9wZG93biBlbGVtZW50LlxuICovXG5jb25zdCBDU1ZfREVMSU1JVEVSX0RST1BET1dOX0NMQVNTID0gJ2pwLUNTVkRlbGltaXRlci1kcm9wZG93bic7XG5cbi8qKlxuICogQSB3aWRnZXQgZm9yIHNlbGVjdGluZyBhIGRlbGltaXRlci5cbiAqL1xuZXhwb3J0IGNsYXNzIENTVkRlbGltaXRlciBleHRlbmRzIFdpZGdldCB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgY3N2IHRhYmxlIHdpZGdldC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IENTVlRvb2xiYXIuSU9wdGlvbnMpIHtcbiAgICBzdXBlcih7IG5vZGU6IFByaXZhdGUuY3JlYXRlTm9kZShvcHRpb25zLnNlbGVjdGVkLCBvcHRpb25zLnRyYW5zbGF0b3IpIH0pO1xuICAgIHRoaXMuYWRkQ2xhc3MoQ1NWX0RFTElNSVRFUl9DTEFTUyk7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBkZWxpbWl0ZXIgc2VsZWN0aW9uIGhhcyBjaGFuZ2VkLlxuICAgKi9cbiAgZ2V0IGRlbGltaXRlckNoYW5nZWQoKTogSVNpZ25hbDx0aGlzLCBzdHJpbmc+IHtcbiAgICByZXR1cm4gdGhpcy5fZGVsaW1pdGVyQ2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVsaW1pdGVyIGRyb3Bkb3duIG1lbnUuXG4gICAqL1xuICBnZXQgc2VsZWN0Tm9kZSgpOiBIVE1MU2VsZWN0RWxlbWVudCB7XG4gICAgcmV0dXJuIHRoaXMubm9kZS5nZXRFbGVtZW50c0J5VGFnTmFtZSgnc2VsZWN0JykhWzBdO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgRE9NIGV2ZW50cyBmb3IgdGhlIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIGV2ZW50IC0gVGhlIERPTSBldmVudCBzZW50IHRvIHRoZSB3aWRnZXQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBtZXRob2QgaW1wbGVtZW50cyB0aGUgRE9NIGBFdmVudExpc3RlbmVyYCBpbnRlcmZhY2UgYW5kIGlzXG4gICAqIGNhbGxlZCBpbiByZXNwb25zZSB0byBldmVudHMgb24gdGhlIGRvY2sgcGFuZWwncyBub2RlLiBJdCBzaG91bGRcbiAgICogbm90IGJlIGNhbGxlZCBkaXJlY3RseSBieSB1c2VyIGNvZGUuXG4gICAqL1xuICBoYW5kbGVFdmVudChldmVudDogRXZlbnQpOiB2b2lkIHtcbiAgICBzd2l0Y2ggKGV2ZW50LnR5cGUpIHtcbiAgICAgIGNhc2UgJ2NoYW5nZSc6XG4gICAgICAgIHRoaXMuX2RlbGltaXRlckNoYW5nZWQuZW1pdCh0aGlzLnNlbGVjdE5vZGUudmFsdWUpO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGFmdGVyLWF0dGFjaGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BZnRlckF0dGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICB0aGlzLnNlbGVjdE5vZGUuYWRkRXZlbnRMaXN0ZW5lcignY2hhbmdlJywgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBiZWZvcmUtZGV0YWNoYCBtZXNzYWdlcyBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByb3RlY3RlZCBvbkJlZm9yZURldGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICB0aGlzLnNlbGVjdE5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcignY2hhbmdlJywgdGhpcyk7XG4gIH1cblxuICBwcml2YXRlIF9kZWxpbWl0ZXJDaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBzdHJpbmc+KHRoaXMpO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBgQ1NWVG9vbGJhcmAgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBDU1ZUb29sYmFyIHtcbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGEgQ1NWIHRvb2xiYXIuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgaW5pdGlhbGx5IHNlbGVjdGVkIGRlbGltaXRlci5cbiAgICAgKi9cbiAgICBzZWxlY3RlZDogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGFwcGxpY2F0aW9uIGxhbmd1YWdlIHRyYW5zbGF0b3IuXG4gICAgICovXG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuICB9XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgdG9vbGJhciBtZXRob2RzLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBDcmVhdGUgdGhlIG5vZGUgZm9yIHRoZSBkZWxpbWl0ZXIgc3dpdGNoZXIuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gY3JlYXRlTm9kZShcbiAgICBzZWxlY3RlZDogc3RyaW5nLFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApOiBIVE1MRWxlbWVudCB7XG4gICAgdHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yPy5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgICAvLyBUaGUgc3VwcG9ydGVkIHBhcnNpbmcgZGVsaW1pdGVycyBhbmQgbGFiZWxzLlxuICAgIGNvbnN0IGRlbGltaXRlcnMgPSBbXG4gICAgICBbJywnLCAnLCddLFxuICAgICAgWyc7JywgJzsnXSxcbiAgICAgIFsnXFx0JywgdHJhbnMuX18oJ3RhYicpXSxcbiAgICAgIFsnfCcsIHRyYW5zLl9fKCdwaXBlJyldLFxuICAgICAgWycjJywgdHJhbnMuX18oJ2hhc2gnKV1cbiAgICBdO1xuXG4gICAgY29uc3QgZGl2ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG4gICAgY29uc3QgbGFiZWwgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdzcGFuJyk7XG4gICAgY29uc3Qgc2VsZWN0ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnc2VsZWN0Jyk7XG4gICAgbGFiZWwudGV4dENvbnRlbnQgPSB0cmFucy5fXygnRGVsaW1pdGVyOiAnKTtcbiAgICBsYWJlbC5jbGFzc05hbWUgPSBDU1ZfREVMSU1JVEVSX0xBQkVMX0NMQVNTO1xuICAgIGVhY2goZGVsaW1pdGVycywgKFtkZWxpbWl0ZXIsIGxhYmVsXSkgPT4ge1xuICAgICAgY29uc3Qgb3B0aW9uID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnb3B0aW9uJyk7XG4gICAgICBvcHRpb24udmFsdWUgPSBkZWxpbWl0ZXI7XG4gICAgICBvcHRpb24udGV4dENvbnRlbnQgPSBsYWJlbDtcbiAgICAgIGlmIChkZWxpbWl0ZXIgPT09IHNlbGVjdGVkKSB7XG4gICAgICAgIG9wdGlvbi5zZWxlY3RlZCA9IHRydWU7XG4gICAgICB9XG4gICAgICBzZWxlY3QuYXBwZW5kQ2hpbGQob3B0aW9uKTtcbiAgICB9KTtcbiAgICBkaXYuYXBwZW5kQ2hpbGQobGFiZWwpO1xuICAgIGNvbnN0IG5vZGUgPSBTdHlsaW5nLndyYXBTZWxlY3Qoc2VsZWN0KTtcbiAgICBub2RlLmNsYXNzTGlzdC5hZGQoQ1NWX0RFTElNSVRFUl9EUk9QRE9XTl9DTEFTUyk7XG4gICAgZGl2LmFwcGVuZENoaWxkKG5vZGUpO1xuICAgIHJldHVybiBkaXY7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgQWN0aXZpdHlNb25pdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7XG4gIEFCQ1dpZGdldEZhY3RvcnksXG4gIERvY3VtZW50UmVnaXN0cnksXG4gIERvY3VtZW50V2lkZ2V0LFxuICBJRG9jdW1lbnRXaWRnZXRcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBQcm9taXNlRGVsZWdhdGUgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQge1xuICBCYXNpY0tleUhhbmRsZXIsXG4gIEJhc2ljTW91c2VIYW5kbGVyLFxuICBCYXNpY1NlbGVjdGlvbk1vZGVsLFxuICBDZWxsUmVuZGVyZXIsXG4gIERhdGFHcmlkLFxuICBUZXh0UmVuZGVyZXJcbn0gZnJvbSAnQGx1bWluby9kYXRhZ3JpZCc7XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgUGFuZWxMYXlvdXQsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBEU1ZNb2RlbCB9IGZyb20gJy4vbW9kZWwnO1xuaW1wb3J0IHsgQ1NWRGVsaW1pdGVyIH0gZnJvbSAnLi90b29sYmFyJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhIENTViB2aWV3ZXIuXG4gKi9cbmNvbnN0IENTVl9DTEFTUyA9ICdqcC1DU1ZWaWV3ZXInO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGEgQ1NWIHZpZXdlciBkYXRhZ3JpZC5cbiAqL1xuY29uc3QgQ1NWX0dSSURfQ0xBU1MgPSAnanAtQ1NWVmlld2VyLWdyaWQnO1xuXG4vKipcbiAqIFRoZSB0aW1lb3V0IHRvIHdhaXQgZm9yIGNoYW5nZSBhY3Rpdml0eSB0byBoYXZlIGNlYXNlZCBiZWZvcmUgcmVuZGVyaW5nLlxuICovXG5jb25zdCBSRU5ERVJfVElNRU9VVCA9IDEwMDA7XG5cbi8qKlxuICogQ29uZmlndXJhdGlvbiBmb3IgY2VsbHMgdGV4dHJlbmRlcmVyLlxuICovXG5leHBvcnQgY2xhc3MgVGV4dFJlbmRlckNvbmZpZyB7XG4gIC8qKlxuICAgKiBkZWZhdWx0IHRleHQgY29sb3JcbiAgICovXG4gIHRleHRDb2xvcjogc3RyaW5nO1xuICAvKipcbiAgICogYmFja2dyb3VuZCBjb2xvciBmb3IgYSBzZWFyY2ggbWF0Y2hcbiAgICovXG4gIG1hdGNoQmFja2dyb3VuZENvbG9yOiBzdHJpbmc7XG4gIC8qKlxuICAgKiBiYWNrZ3JvdW5kIGNvbG9yIGZvciB0aGUgY3VycmVudCBzZWFyY2ggbWF0Y2guXG4gICAqL1xuICBjdXJyZW50TWF0Y2hCYWNrZ3JvdW5kQ29sb3I6IHN0cmluZztcbiAgLyoqXG4gICAqIGhvcml6b250YWxBbGlnbm1lbnQgb2YgdGhlIHRleHRcbiAgICovXG4gIGhvcml6b250YWxBbGlnbm1lbnQ6IFRleHRSZW5kZXJlci5Ib3Jpem9udGFsQWxpZ25tZW50O1xufVxuXG4vKipcbiAqIFNlYXJjaCBzZXJ2aWNlIHJlbWVtYmVycyB0aGUgc2VhcmNoIHN0YXRlIGFuZCB0aGUgbG9jYXRpb24gb2YgdGhlIGxhc3RcbiAqIG1hdGNoLCBmb3IgaW5jcmVtZW50YWwgc2VhcmNoaW5nLlxuICogU2VhcmNoIHNlcnZpY2UgaXMgYWxzbyByZXNwb25zaWJsZSBvZiBwcm92aWRpbmcgYSBjZWxsIHJlbmRlcmVyIGZ1bmN0aW9uXG4gKiB0byBzZXQgdGhlIGJhY2tncm91bmQgY29sb3Igb2YgY2VsbHMgbWF0Y2hpbmcgdGhlIHNlYXJjaCB0ZXh0LlxuICovXG5leHBvcnQgY2xhc3MgR3JpZFNlYXJjaFNlcnZpY2Uge1xuICBjb25zdHJ1Y3RvcihncmlkOiBEYXRhR3JpZCkge1xuICAgIHRoaXMuX2dyaWQgPSBncmlkO1xuICAgIHRoaXMuX3F1ZXJ5ID0gbnVsbDtcbiAgICB0aGlzLl9yb3cgPSAwO1xuICAgIHRoaXMuX2NvbHVtbiA9IC0xO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGZpcmVkIHdoZW4gdGhlIGdyaWQgY2hhbmdlcy5cbiAgICovXG4gIGdldCBjaGFuZ2VkKCk6IElTaWduYWw8R3JpZFNlYXJjaFNlcnZpY2UsIHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5fY2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXR1cm5zIGEgY2VsbHJlbmRlcmVyIGNvbmZpZyBmdW5jdGlvbiB0byByZW5kZXIgZWFjaCBjZWxsIGJhY2tncm91bmQuXG4gICAqIElmIGNlbGwgbWF0Y2gsIGJhY2tncm91bmQgaXMgbWF0Y2hCYWNrZ3JvdW5kQ29sb3IsIGlmIGl0J3MgdGhlIGN1cnJlbnRcbiAgICogbWF0Y2gsIGJhY2tncm91bmQgaXMgY3VycmVudE1hdGNoQmFja2dyb3VuZENvbG9yLlxuICAgKi9cbiAgY2VsbEJhY2tncm91bmRDb2xvclJlbmRlcmVyRnVuYyhcbiAgICBjb25maWc6IFRleHRSZW5kZXJDb25maWdcbiAgKTogQ2VsbFJlbmRlcmVyLkNvbmZpZ0Z1bmM8c3RyaW5nPiB7XG4gICAgcmV0dXJuICh7IHZhbHVlLCByb3csIGNvbHVtbiB9KSA9PiB7XG4gICAgICBpZiAodGhpcy5fcXVlcnkpIHtcbiAgICAgICAgaWYgKCh2YWx1ZSBhcyBzdHJpbmcpLm1hdGNoKHRoaXMuX3F1ZXJ5KSkge1xuICAgICAgICAgIGlmICh0aGlzLl9yb3cgPT09IHJvdyAmJiB0aGlzLl9jb2x1bW4gPT09IGNvbHVtbikge1xuICAgICAgICAgICAgcmV0dXJuIGNvbmZpZy5jdXJyZW50TWF0Y2hCYWNrZ3JvdW5kQ29sb3I7XG4gICAgICAgICAgfVxuICAgICAgICAgIHJldHVybiBjb25maWcubWF0Y2hCYWNrZ3JvdW5kQ29sb3I7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIHJldHVybiAnJztcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIENsZWFyIHRoZSBzZWFyY2guXG4gICAqL1xuICBjbGVhcigpIHtcbiAgICB0aGlzLl9xdWVyeSA9IG51bGw7XG4gICAgdGhpcy5fcm93ID0gMDtcbiAgICB0aGlzLl9jb2x1bW4gPSAtMTtcbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQodW5kZWZpbmVkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBpbmNyZW1lbnRhbGx5IGxvb2sgZm9yIHNlYXJjaFRleHQuXG4gICAqL1xuICBmaW5kKHF1ZXJ5OiBSZWdFeHAsIHJldmVyc2UgPSBmYWxzZSk6IGJvb2xlYW4ge1xuICAgIGNvbnN0IG1vZGVsID0gdGhpcy5fZ3JpZC5kYXRhTW9kZWwhO1xuICAgIGNvbnN0IHJvd0NvdW50ID0gbW9kZWwucm93Q291bnQoJ2JvZHknKTtcbiAgICBjb25zdCBjb2x1bW5Db3VudCA9IG1vZGVsLmNvbHVtbkNvdW50KCdib2R5Jyk7XG5cbiAgICBpZiAodGhpcy5fcXVlcnkgIT09IHF1ZXJ5KSB7XG4gICAgICAvLyByZXNldCBzZWFyY2hcbiAgICAgIHRoaXMuX3JvdyA9IDA7XG4gICAgICB0aGlzLl9jb2x1bW4gPSAtMTtcbiAgICB9XG4gICAgdGhpcy5fcXVlcnkgPSBxdWVyeTtcblxuICAgIC8vIGNoZWNrIGlmIHRoZSBtYXRjaCBpcyBpbiBjdXJyZW50IHZpZXdwb3J0XG5cbiAgICBjb25zdCBtaW5Sb3cgPSB0aGlzLl9ncmlkLnNjcm9sbFkgLyB0aGlzLl9ncmlkLmRlZmF1bHRTaXplcy5yb3dIZWlnaHQ7XG4gICAgY29uc3QgbWF4Um93ID1cbiAgICAgICh0aGlzLl9ncmlkLnNjcm9sbFkgKyB0aGlzLl9ncmlkLnBhZ2VIZWlnaHQpIC9cbiAgICAgIHRoaXMuX2dyaWQuZGVmYXVsdFNpemVzLnJvd0hlaWdodDtcbiAgICBjb25zdCBtaW5Db2x1bW4gPVxuICAgICAgdGhpcy5fZ3JpZC5zY3JvbGxYIC8gdGhpcy5fZ3JpZC5kZWZhdWx0U2l6ZXMuY29sdW1uSGVhZGVySGVpZ2h0O1xuICAgIGNvbnN0IG1heENvbHVtbiA9XG4gICAgICAodGhpcy5fZ3JpZC5zY3JvbGxYICsgdGhpcy5fZ3JpZC5wYWdlV2lkdGgpIC9cbiAgICAgIHRoaXMuX2dyaWQuZGVmYXVsdFNpemVzLmNvbHVtbkhlYWRlckhlaWdodDtcbiAgICBjb25zdCBpc0luVmlld3BvcnQgPSAocm93OiBudW1iZXIsIGNvbHVtbjogbnVtYmVyKSA9PiB7XG4gICAgICByZXR1cm4gKFxuICAgICAgICByb3cgPj0gbWluUm93ICYmXG4gICAgICAgIHJvdyA8PSBtYXhSb3cgJiZcbiAgICAgICAgY29sdW1uID49IG1pbkNvbHVtbiAmJlxuICAgICAgICBjb2x1bW4gPD0gbWF4Q29sdW1uXG4gICAgICApO1xuICAgIH07XG5cbiAgICBjb25zdCBpbmNyZW1lbnQgPSByZXZlcnNlID8gLTEgOiAxO1xuICAgIHRoaXMuX2NvbHVtbiArPSBpbmNyZW1lbnQ7XG4gICAgZm9yIChcbiAgICAgIGxldCByb3cgPSB0aGlzLl9yb3c7XG4gICAgICByZXZlcnNlID8gcm93ID49IDAgOiByb3cgPCByb3dDb3VudDtcbiAgICAgIHJvdyArPSBpbmNyZW1lbnRcbiAgICApIHtcbiAgICAgIGZvciAoXG4gICAgICAgIGxldCBjb2wgPSB0aGlzLl9jb2x1bW47XG4gICAgICAgIHJldmVyc2UgPyBjb2wgPj0gMCA6IGNvbCA8IGNvbHVtbkNvdW50O1xuICAgICAgICBjb2wgKz0gaW5jcmVtZW50XG4gICAgICApIHtcbiAgICAgICAgY29uc3QgY2VsbERhdGEgPSBtb2RlbC5kYXRhKCdib2R5Jywgcm93LCBjb2wpIGFzIHN0cmluZztcbiAgICAgICAgaWYgKGNlbGxEYXRhLm1hdGNoKHF1ZXJ5KSkge1xuICAgICAgICAgIC8vIHRvIHVwZGF0ZSB0aGUgYmFja2dyb3VuZCBvZiBtYXRjaGluZyBjZWxscy5cblxuICAgICAgICAgIC8vIFRPRE86IHdlIG9ubHkgcmVhbGx5IG5lZWQgdG8gaW52YWxpZGF0ZSB0aGUgcHJldmlvdXMgYW5kIGN1cnJlbnRcbiAgICAgICAgICAvLyBjZWxsIHJlY3RzLCBub3QgdGhlIGVudGlyZSBncmlkLlxuICAgICAgICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh1bmRlZmluZWQpO1xuXG4gICAgICAgICAgaWYgKCFpc0luVmlld3BvcnQocm93LCBjb2wpKSB7XG4gICAgICAgICAgICB0aGlzLl9ncmlkLnNjcm9sbFRvUm93KHJvdyk7XG4gICAgICAgICAgfVxuICAgICAgICAgIHRoaXMuX3JvdyA9IHJvdztcbiAgICAgICAgICB0aGlzLl9jb2x1bW4gPSBjb2w7XG4gICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIHRoaXMuX2NvbHVtbiA9IHJldmVyc2UgPyBjb2x1bW5Db3VudCAtIDEgOiAwO1xuICAgIH1cbiAgICAvLyBXZSd2ZSBmaW5pc2hlZCBzZWFyY2hpbmcgYWxsIHRoZSB3YXkgdG8gdGhlIGxpbWl0cyBvZiB0aGUgZ3JpZC4gSWYgdGhpc1xuICAgIC8vIGlzIHRoZSBmaXJzdCB0aW1lIHRocm91Z2ggKGxvb3BpbmcgaXMgdHJ1ZSksIHdyYXAgdGhlIGluZGljZXMgYW5kIHNlYXJjaFxuICAgIC8vIGFnYWluLiBPdGhlcndpc2UsIGdpdmUgdXAuXG4gICAgaWYgKHRoaXMuX2xvb3BpbmcpIHtcbiAgICAgIHRoaXMuX2xvb3BpbmcgPSBmYWxzZTtcbiAgICAgIHRoaXMuX3JvdyA9IHJldmVyc2UgPyAwIDogcm93Q291bnQgLSAxO1xuICAgICAgdGhpcy5fd3JhcFJvd3MocmV2ZXJzZSk7XG4gICAgICB0cnkge1xuICAgICAgICByZXR1cm4gdGhpcy5maW5kKHF1ZXJ5LCByZXZlcnNlKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIHRoaXMuX2xvb3BpbmcgPSB0cnVlO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cblxuICAvKipcbiAgICogV3JhcCBpbmRpY2VzIGlmIG5lZWRlZCB0byBqdXN0IGJlZm9yZSB0aGUgc3RhcnQgb3IganVzdCBhZnRlciB0aGUgZW5kLlxuICAgKi9cbiAgcHJpdmF0ZSBfd3JhcFJvd3MocmV2ZXJzZSA9IGZhbHNlKSB7XG4gICAgY29uc3QgbW9kZWwgPSB0aGlzLl9ncmlkLmRhdGFNb2RlbCE7XG4gICAgY29uc3Qgcm93Q291bnQgPSBtb2RlbC5yb3dDb3VudCgnYm9keScpO1xuICAgIGNvbnN0IGNvbHVtbkNvdW50ID0gbW9kZWwuY29sdW1uQ291bnQoJ2JvZHknKTtcblxuICAgIGlmIChyZXZlcnNlICYmIHRoaXMuX3JvdyA8PSAwKSB7XG4gICAgICAvLyBpZiB3ZSBhcmUgYXQgdGhlIGZyb250LCB3cmFwIHRvIGp1c3QgcGFzdCB0aGUgZW5kLlxuICAgICAgdGhpcy5fcm93ID0gcm93Q291bnQgLSAxO1xuICAgICAgdGhpcy5fY29sdW1uID0gY29sdW1uQ291bnQ7XG4gICAgfSBlbHNlIGlmICghcmV2ZXJzZSAmJiB0aGlzLl9yb3cgPj0gcm93Q291bnQgLSAxKSB7XG4gICAgICAvLyBpZiB3ZSBhcmUgYXQgdGhlIGVuZCwgd3JhcCB0byBqdXN0IGJlZm9yZSB0aGUgZnJvbnQuXG4gICAgICB0aGlzLl9yb3cgPSAwO1xuICAgICAgdGhpcy5fY29sdW1uID0gLTE7XG4gICAgfVxuICB9XG5cbiAgZ2V0IHF1ZXJ5KCk6IFJlZ0V4cCB8IG51bGwge1xuICAgIHJldHVybiB0aGlzLl9xdWVyeTtcbiAgfVxuXG4gIHByaXZhdGUgX2dyaWQ6IERhdGFHcmlkO1xuICBwcml2YXRlIF9xdWVyeTogUmVnRXhwIHwgbnVsbDtcbiAgcHJpdmF0ZSBfcm93OiBudW1iZXI7XG4gIHByaXZhdGUgX2NvbHVtbjogbnVtYmVyO1xuICBwcml2YXRlIF9sb29waW5nID0gdHJ1ZTtcbiAgcHJpdmF0ZSBfY2hhbmdlZCA9IG5ldyBTaWduYWw8R3JpZFNlYXJjaFNlcnZpY2UsIHZvaWQ+KHRoaXMpO1xufVxuXG4vKipcbiAqIEEgdmlld2VyIGZvciBDU1YgdGFibGVzLlxuICovXG5leHBvcnQgY2xhc3MgQ1NWVmlld2VyIGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBDU1Ygdmlld2VyLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogQ1NWVmlld2VyLklPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcblxuICAgIGNvbnN0IGNvbnRleHQgPSAodGhpcy5fY29udGV4dCA9IG9wdGlvbnMuY29udGV4dCk7XG4gICAgY29uc3QgbGF5b3V0ID0gKHRoaXMubGF5b3V0ID0gbmV3IFBhbmVsTGF5b3V0KCkpO1xuXG4gICAgdGhpcy5hZGRDbGFzcyhDU1ZfQ0xBU1MpO1xuXG4gICAgdGhpcy5fZ3JpZCA9IG5ldyBEYXRhR3JpZCh7XG4gICAgICBkZWZhdWx0U2l6ZXM6IHtcbiAgICAgICAgcm93SGVpZ2h0OiAyNCxcbiAgICAgICAgY29sdW1uV2lkdGg6IDE0NCxcbiAgICAgICAgcm93SGVhZGVyV2lkdGg6IDY0LFxuICAgICAgICBjb2x1bW5IZWFkZXJIZWlnaHQ6IDM2XG4gICAgICB9XG4gICAgfSk7XG4gICAgdGhpcy5fZ3JpZC5hZGRDbGFzcyhDU1ZfR1JJRF9DTEFTUyk7XG4gICAgdGhpcy5fZ3JpZC5oZWFkZXJWaXNpYmlsaXR5ID0gJ2FsbCc7XG4gICAgdGhpcy5fZ3JpZC5rZXlIYW5kbGVyID0gbmV3IEJhc2ljS2V5SGFuZGxlcigpO1xuICAgIHRoaXMuX2dyaWQubW91c2VIYW5kbGVyID0gbmV3IEJhc2ljTW91c2VIYW5kbGVyKCk7XG4gICAgdGhpcy5fZ3JpZC5jb3B5Q29uZmlnID0ge1xuICAgICAgc2VwYXJhdG9yOiAnXFx0JyxcbiAgICAgIGZvcm1hdDogRGF0YUdyaWQuY29weUZvcm1hdEdlbmVyaWMsXG4gICAgICBoZWFkZXJzOiAnYWxsJyxcbiAgICAgIHdhcm5pbmdUaHJlc2hvbGQ6IDFlNlxuICAgIH07XG5cbiAgICBsYXlvdXQuYWRkV2lkZ2V0KHRoaXMuX2dyaWQpO1xuXG4gICAgdGhpcy5fc2VhcmNoU2VydmljZSA9IG5ldyBHcmlkU2VhcmNoU2VydmljZSh0aGlzLl9ncmlkKTtcbiAgICB0aGlzLl9zZWFyY2hTZXJ2aWNlLmNoYW5nZWQuY29ubmVjdCh0aGlzLl91cGRhdGVSZW5kZXJlciwgdGhpcyk7XG5cbiAgICB2b2lkIHRoaXMuX2NvbnRleHQucmVhZHkudGhlbigoKSA9PiB7XG4gICAgICB0aGlzLl91cGRhdGVHcmlkKCk7XG4gICAgICB0aGlzLl9yZXZlYWxlZC5yZXNvbHZlKHVuZGVmaW5lZCk7XG4gICAgICAvLyBUaHJvdHRsZSB0aGUgcmVuZGVyaW5nIHJhdGUgb2YgdGhlIHdpZGdldC5cbiAgICAgIHRoaXMuX21vbml0b3IgPSBuZXcgQWN0aXZpdHlNb25pdG9yKHtcbiAgICAgICAgc2lnbmFsOiBjb250ZXh0Lm1vZGVsLmNvbnRlbnRDaGFuZ2VkLFxuICAgICAgICB0aW1lb3V0OiBSRU5ERVJfVElNRU9VVFxuICAgICAgfSk7XG4gICAgICB0aGlzLl9tb25pdG9yLmFjdGl2aXR5U3RvcHBlZC5jb25uZWN0KHRoaXMuX3VwZGF0ZUdyaWQsIHRoaXMpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBDU1Ygd2lkZ2V0J3MgY29udGV4dC5cbiAgICovXG4gIGdldCBjb250ZXh0KCk6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dCB7XG4gICAgcmV0dXJuIHRoaXMuX2NvbnRleHQ7XG4gIH1cblxuICAvKipcbiAgICogQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgY3N2IHZpZXdlciBpcyByZWFkeSB0byBiZSByZXZlYWxlZC5cbiAgICovXG4gIGdldCByZXZlYWxlZCgpIHtcbiAgICByZXR1cm4gdGhpcy5fcmV2ZWFsZWQucHJvbWlzZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVsaW1pdGVyIGZvciB0aGUgZmlsZS5cbiAgICovXG4gIGdldCBkZWxpbWl0ZXIoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5fZGVsaW1pdGVyO1xuICB9XG4gIHNldCBkZWxpbWl0ZXIodmFsdWU6IHN0cmluZykge1xuICAgIGlmICh2YWx1ZSA9PT0gdGhpcy5fZGVsaW1pdGVyKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2RlbGltaXRlciA9IHZhbHVlO1xuICAgIHRoaXMuX3VwZGF0ZUdyaWQoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgc3R5bGUgdXNlZCBieSB0aGUgZGF0YSBncmlkLlxuICAgKi9cbiAgZ2V0IHN0eWxlKCk6IERhdGFHcmlkLlN0eWxlIHtcbiAgICByZXR1cm4gdGhpcy5fZ3JpZC5zdHlsZTtcbiAgfVxuICBzZXQgc3R5bGUodmFsdWU6IERhdGFHcmlkLlN0eWxlKSB7XG4gICAgdGhpcy5fZ3JpZC5zdHlsZSA9IHZhbHVlO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjb25maWcgdXNlZCB0byBjcmVhdGUgdGV4dCByZW5kZXJlci5cbiAgICovXG4gIHNldCByZW5kZXJlckNvbmZpZyhyZW5kZXJlckNvbmZpZzogVGV4dFJlbmRlckNvbmZpZykge1xuICAgIHRoaXMuX2Jhc2VSZW5kZXJlciA9IHJlbmRlcmVyQ29uZmlnO1xuICAgIHRoaXMuX3VwZGF0ZVJlbmRlcmVyKCk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNlYXJjaCBzZXJ2aWNlXG4gICAqL1xuICBnZXQgc2VhcmNoU2VydmljZSgpOiBHcmlkU2VhcmNoU2VydmljZSB7XG4gICAgcmV0dXJuIHRoaXMuX3NlYXJjaFNlcnZpY2U7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIHVzZWQgYnkgdGhlIHdpZGdldC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX21vbml0b3IpIHtcbiAgICAgIHRoaXMuX21vbml0b3IuZGlzcG9zZSgpO1xuICAgIH1cbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogR28gdG8gbGluZVxuICAgKi9cbiAgZ29Ub0xpbmUobGluZU51bWJlcjogbnVtYmVyKSB7XG4gICAgdGhpcy5fZ3JpZC5zY3JvbGxUb1JvdyhsaW5lTnVtYmVyKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdhY3RpdmF0ZS1yZXF1ZXN0J2AgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BY3RpdmF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5ub2RlLnRhYkluZGV4ID0gLTE7XG4gICAgdGhpcy5ub2RlLmZvY3VzKCk7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIHRoZSBtb2RlbCBmb3IgdGhlIGdyaWQuXG4gICAqL1xuICBwcml2YXRlIF91cGRhdGVHcmlkKCk6IHZvaWQge1xuICAgIGNvbnN0IGRhdGE6IHN0cmluZyA9IHRoaXMuX2NvbnRleHQubW9kZWwudG9TdHJpbmcoKTtcbiAgICBjb25zdCBkZWxpbWl0ZXIgPSB0aGlzLl9kZWxpbWl0ZXI7XG4gICAgY29uc3Qgb2xkTW9kZWwgPSB0aGlzLl9ncmlkLmRhdGFNb2RlbCBhcyBEU1ZNb2RlbDtcbiAgICBjb25zdCBkYXRhTW9kZWwgPSAodGhpcy5fZ3JpZC5kYXRhTW9kZWwgPSBuZXcgRFNWTW9kZWwoe1xuICAgICAgZGF0YSxcbiAgICAgIGRlbGltaXRlclxuICAgIH0pKTtcbiAgICB0aGlzLl9ncmlkLnNlbGVjdGlvbk1vZGVsID0gbmV3IEJhc2ljU2VsZWN0aW9uTW9kZWwoeyBkYXRhTW9kZWwgfSk7XG4gICAgaWYgKG9sZE1vZGVsKSB7XG4gICAgICBvbGRNb2RlbC5kaXNwb3NlKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSB0aGUgcmVuZGVyZXIgZm9yIHRoZSBncmlkLlxuICAgKi9cbiAgcHJpdmF0ZSBfdXBkYXRlUmVuZGVyZXIoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX2Jhc2VSZW5kZXJlciA9PT0gbnVsbCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCByZW5kZXJlckNvbmZpZyA9IHRoaXMuX2Jhc2VSZW5kZXJlcjtcbiAgICBjb25zdCByZW5kZXJlciA9IG5ldyBUZXh0UmVuZGVyZXIoe1xuICAgICAgdGV4dENvbG9yOiByZW5kZXJlckNvbmZpZy50ZXh0Q29sb3IsXG4gICAgICBob3Jpem9udGFsQWxpZ25tZW50OiByZW5kZXJlckNvbmZpZy5ob3Jpem9udGFsQWxpZ25tZW50LFxuICAgICAgYmFja2dyb3VuZENvbG9yOiB0aGlzLl9zZWFyY2hTZXJ2aWNlLmNlbGxCYWNrZ3JvdW5kQ29sb3JSZW5kZXJlckZ1bmMoXG4gICAgICAgIHJlbmRlcmVyQ29uZmlnXG4gICAgICApXG4gICAgfSk7XG4gICAgdGhpcy5fZ3JpZC5jZWxsUmVuZGVyZXJzLnVwZGF0ZSh7XG4gICAgICBib2R5OiByZW5kZXJlcixcbiAgICAgICdjb2x1bW4taGVhZGVyJzogcmVuZGVyZXIsXG4gICAgICAnY29ybmVyLWhlYWRlcic6IHJlbmRlcmVyLFxuICAgICAgJ3Jvdy1oZWFkZXInOiByZW5kZXJlclxuICAgIH0pO1xuICB9XG5cbiAgcHJpdmF0ZSBfY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0O1xuICBwcml2YXRlIF9ncmlkOiBEYXRhR3JpZDtcbiAgcHJpdmF0ZSBfc2VhcmNoU2VydmljZTogR3JpZFNlYXJjaFNlcnZpY2U7XG4gIHByaXZhdGUgX21vbml0b3I6IEFjdGl2aXR5TW9uaXRvcjxcbiAgICBEb2N1bWVudFJlZ2lzdHJ5LklNb2RlbCxcbiAgICB2b2lkXG4gID4gfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfZGVsaW1pdGVyID0gJywnO1xuICBwcml2YXRlIF9yZXZlYWxlZCA9IG5ldyBQcm9taXNlRGVsZWdhdGU8dm9pZD4oKTtcbiAgcHJpdmF0ZSBfYmFzZVJlbmRlcmVyOiBUZXh0UmVuZGVyQ29uZmlnIHwgbnVsbCA9IG51bGw7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIGBDU1ZWaWV3ZXJgIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgQ1NWVmlld2VyIHtcbiAgLyoqXG4gICAqIEluc3RhbnRpYXRpb24gb3B0aW9ucyBmb3IgQ1NWIHdpZGdldHMuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgZG9jdW1lbnQgY29udGV4dCBmb3IgdGhlIENTViBiZWluZyByZW5kZXJlZCBieSB0aGUgd2lkZ2V0LlxuICAgICAqL1xuICAgIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dDtcbiAgfVxufVxuXG4vKipcbiAqIEEgZG9jdW1lbnQgd2lkZ2V0IGZvciBDU1YgY29udGVudCB3aWRnZXRzLlxuICovXG5leHBvcnQgY2xhc3MgQ1NWRG9jdW1lbnRXaWRnZXQgZXh0ZW5kcyBEb2N1bWVudFdpZGdldDxDU1ZWaWV3ZXI+IHtcbiAgY29uc3RydWN0b3Iob3B0aW9uczogQ1NWRG9jdW1lbnRXaWRnZXQuSU9wdGlvbnMpIHtcbiAgICBsZXQgeyBjb250ZW50LCBjb250ZXh0LCBkZWxpbWl0ZXIsIHJldmVhbCwgLi4ub3RoZXIgfSA9IG9wdGlvbnM7XG4gICAgY29udGVudCA9IGNvbnRlbnQgfHwgUHJpdmF0ZS5jcmVhdGVDb250ZW50KGNvbnRleHQpO1xuICAgIHJldmVhbCA9IFByb21pc2UuYWxsKFtyZXZlYWwsIGNvbnRlbnQucmV2ZWFsZWRdKTtcbiAgICBzdXBlcih7IGNvbnRlbnQsIGNvbnRleHQsIHJldmVhbCwgLi4ub3RoZXIgfSk7XG5cbiAgICBpZiAoZGVsaW1pdGVyKSB7XG4gICAgICBjb250ZW50LmRlbGltaXRlciA9IGRlbGltaXRlcjtcbiAgICB9XG4gICAgY29uc3QgY3N2RGVsaW1pdGVyID0gbmV3IENTVkRlbGltaXRlcih7IHNlbGVjdGVkOiBjb250ZW50LmRlbGltaXRlciB9KTtcbiAgICB0aGlzLnRvb2xiYXIuYWRkSXRlbSgnZGVsaW1pdGVyJywgY3N2RGVsaW1pdGVyKTtcbiAgICBjc3ZEZWxpbWl0ZXIuZGVsaW1pdGVyQ2hhbmdlZC5jb25uZWN0KFxuICAgICAgKHNlbmRlcjogQ1NWRGVsaW1pdGVyLCBkZWxpbWl0ZXI6IHN0cmluZykgPT4ge1xuICAgICAgICBjb250ZW50IS5kZWxpbWl0ZXIgPSBkZWxpbWl0ZXI7XG4gICAgICB9XG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgVVJJIGZyYWdtZW50IGlkZW50aWZpZXIgZm9yIHJvd3NcbiAgICovXG4gIHNldEZyYWdtZW50KGZyYWdtZW50OiBzdHJpbmcpOiB2b2lkIHtcbiAgICBjb25zdCBwYXJzZUZyYWdtZW50cyA9IGZyYWdtZW50LnNwbGl0KCc9Jyk7XG5cbiAgICAvLyBUT0RPOiBleHBhbmQgdG8gYWxsb3cgY29sdW1ucyBhbmQgY2VsbHMgdG8gYmUgc2VsZWN0ZWRcbiAgICAvLyByZWZlcmVuY2U6IGh0dHBzOi8vdG9vbHMuaWV0Zi5vcmcvaHRtbC9yZmM3MTExI3NlY3Rpb24tM1xuICAgIGlmIChwYXJzZUZyYWdtZW50c1swXSAhPT0gJyNyb3cnKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gbXVsdGlwbGUgcm93cywgc2VwYXJhdGVkIGJ5IHNlbWktY29sb25zIGNhbiBiZSBwcm92aWRlZCwgd2Ugd2lsbCBqdXN0XG4gICAgLy8gZ28gdG8gdGhlIHRvcCBvbmVcbiAgICBsZXQgdG9wUm93ID0gcGFyc2VGcmFnbWVudHNbMV0uc3BsaXQoJzsnKVswXTtcblxuICAgIC8vIGEgcmFuZ2Ugb2Ygcm93cyBjYW4gYmUgcHJvdmlkZWQsIHdlIHdpbGwgdGFrZSB0aGUgZmlyc3QgdmFsdWVcbiAgICB0b3BSb3cgPSB0b3BSb3cuc3BsaXQoJy0nKVswXTtcblxuICAgIC8vIGdvIHRvIHRoYXQgcm93XG4gICAgdm9pZCB0aGlzLmNvbnRleHQucmVhZHkudGhlbigoKSA9PiB7XG4gICAgICB0aGlzLmNvbnRlbnQuZ29Ub0xpbmUoTnVtYmVyKHRvcFJvdykpO1xuICAgIH0pO1xuICB9XG59XG5cbmV4cG9ydCBuYW1lc3BhY2UgQ1NWRG9jdW1lbnRXaWRnZXQge1xuICAvLyBUT0RPOiBJbiBUeXBlU2NyaXB0IDIuOCwgd2UgY2FuIG1ha2UganVzdCB0aGUgY29udGVudCBwcm9wZXJ0eSBvcHRpb25hbFxuICAvLyB1c2luZyBzb21ldGhpbmcgbGlrZSBodHRwczovL3N0YWNrb3ZlcmZsb3cuY29tL2EvNDY5NDE4MjQsIGluc3RlYWQgb2ZcbiAgLy8gaW5oZXJpdGluZyBmcm9tIHRoaXMgSU9wdGlvbnNPcHRpb25hbENvbnRlbnQuXG5cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9uc1xuICAgIGV4dGVuZHMgRG9jdW1lbnRXaWRnZXQuSU9wdGlvbnNPcHRpb25hbENvbnRlbnQ8Q1NWVmlld2VyPiB7XG4gICAgZGVsaW1pdGVyPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGFwcGxpY2F0aW9uIGxhbmd1YWdlIHRyYW5zbGF0b3IuXG4gICAgICovXG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuICB9XG59XG5cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZUNvbnRlbnQoXG4gICAgY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5JQ29udGV4dDxEb2N1bWVudFJlZ2lzdHJ5LklNb2RlbD5cbiAgKSB7XG4gICAgcmV0dXJuIG5ldyBDU1ZWaWV3ZXIoeyBjb250ZXh0IH0pO1xuICB9XG59XG5cbi8qKlxuICogQSB3aWRnZXQgZmFjdG9yeSBmb3IgQ1NWIHdpZGdldHMuXG4gKi9cbmV4cG9ydCBjbGFzcyBDU1ZWaWV3ZXJGYWN0b3J5IGV4dGVuZHMgQUJDV2lkZ2V0RmFjdG9yeTxcbiAgSURvY3VtZW50V2lkZ2V0PENTVlZpZXdlcj5cbj4ge1xuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHdpZGdldCBnaXZlbiBhIGNvbnRleHQuXG4gICAqL1xuICBwcm90ZWN0ZWQgY3JlYXRlTmV3V2lkZ2V0KFxuICAgIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dFxuICApOiBJRG9jdW1lbnRXaWRnZXQ8Q1NWVmlld2VyPiB7XG4gICAgY29uc3QgdHJhbnNsYXRvciA9IHRoaXMudHJhbnNsYXRvcjtcbiAgICByZXR1cm4gbmV3IENTVkRvY3VtZW50V2lkZ2V0KHsgY29udGV4dCwgdHJhbnNsYXRvciB9KTtcbiAgfVxufVxuXG4vKipcbiAqIEEgd2lkZ2V0IGZhY3RvcnkgZm9yIFRTViB3aWRnZXRzLlxuICovXG5leHBvcnQgY2xhc3MgVFNWVmlld2VyRmFjdG9yeSBleHRlbmRzIEFCQ1dpZGdldEZhY3Rvcnk8XG4gIElEb2N1bWVudFdpZGdldDxDU1ZWaWV3ZXI+XG4+IHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyB3aWRnZXQgZ2l2ZW4gYSBjb250ZXh0LlxuICAgKi9cbiAgcHJvdGVjdGVkIGNyZWF0ZU5ld1dpZGdldChcbiAgICBjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHRcbiAgKTogSURvY3VtZW50V2lkZ2V0PENTVlZpZXdlcj4ge1xuICAgIGNvbnN0IGRlbGltaXRlciA9ICdcXHQnO1xuICAgIHJldHVybiBuZXcgQ1NWRG9jdW1lbnRXaWRnZXQoe1xuICAgICAgY29udGV4dCxcbiAgICAgIGRlbGltaXRlcixcbiAgICAgIHRyYW5zbGF0b3I6IHRoaXMudHJhbnNsYXRvclxuICAgIH0pO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9