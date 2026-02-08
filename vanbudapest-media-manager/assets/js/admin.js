/**
 * VanBudapest Media Manager - Admin JavaScript
 */
(function ($) {
    'use strict';

    var VBMM = {
        items: [],
        selectedIds: [],
        currentPage: 1,
        totalPages: 1,
        totalItems: 0,
        currentView: 'grid',
        debounceTimer: null,

        /**
         * Initialize
         */
        init: function () {
            this.bindEvents();
            this.loadMedia();
            this.loadStats();
        },

        /**
         * Bind all event handlers
         */
        bindEvents: function () {
            var self = this;

            // Select all
            $('#vbmm-select-all').on('change', function () {
                self.toggleSelectAll($(this).is(':checked'));
            });

            // Search with debounce
            $('#vbmm-search').on('input', function () {
                clearTimeout(self.debounceTimer);
                self.debounceTimer = setTimeout(function () {
                    self.currentPage = 1;
                    self.loadMedia();
                }, 300);
            });

            // Filters
            $('#vbmm-filter-type, #vbmm-filter-date, #vbmm-filter-size, #vbmm-filter-attached, #vbmm-sort').on('change', function () {
                self.currentPage = 1;
                self.loadMedia();
            });

            // Reset filters
            $('#vbmm-reset-filters').on('click', function () {
                $('#vbmm-search').val('');
                $('#vbmm-filter-type, #vbmm-filter-date, #vbmm-filter-size, #vbmm-filter-attached').val('');
                $('#vbmm-sort').val('date-desc');
                self.currentPage = 1;
                self.loadMedia();
            });

            // View toggle
            $('.vbmm-view-btn').on('click', function () {
                var view = $(this).data('view');
                self.setView(view);
            });

            // Load more
            $('#vbmm-load-more-btn').on('click', function () {
                self.currentPage++;
                self.loadMedia(true);
            });

            // Export buttons
            $(document).on('click', '.vbmm-export-btn', function () {
                var format = $(this).data('format');
                self.showExportModal(format);
            });

            // Copy export
            $('#vbmm-copy-export').on('click', function () {
                self.copyToClipboard($('#vbmm-export-code').val());
            });

            // Download export
            $('#vbmm-download-export').on('click', function () {
                self.downloadExport();
            });

            // Close modal
            $('#vbmm-modal-close, .vbmm-modal-overlay').on('click', function () {
                $('#vbmm-export-modal').hide();
            });

            // Bulk delete
            $('#vbmm-bulk-delete').on('click', function () {
                self.bulkDelete();
            });

            // Bulk optimize
            $('#vbmm-bulk-optimize').on('click', function () {
                self.bulkOptimize();
            });

            // Edit panel close
            $('#vbmm-edit-close').on('click', function () {
                self.closeEditPanel();
            });

            // Edit panel save
            $('#vbmm-edit-save').on('click', function () {
                self.saveEdit();
            });

            // Copy URL in edit panel
            $(document).on('click', '.vbmm-copy-url', function () {
                var url = $(this).siblings('input').val();
                self.copyToClipboard(url);
            });

            // Copy size URL
            $(document).on('click', '.vbmm-size-copy', function (e) {
                e.preventDefault();
                self.copyToClipboard($(this).data('url'));
            });

            // Card click events (delegated)
            $(document).on('click', '.vbmm-card-checkbox', function (e) {
                e.stopPropagation();
                var id = parseInt($(this).closest('.vbmm-media-card').data('id'));
                self.toggleSelect(id, $(this).is(':checked'));
            });

            $(document).on('click', '.vbmm-card-action[data-action="edit"]', function (e) {
                e.stopPropagation();
                var id = parseInt($(this).closest('.vbmm-media-card').data('id'));
                self.openEditPanel(id);
            });

            $(document).on('click', '.vbmm-card-action[data-action="copy"]', function (e) {
                e.stopPropagation();
                var id = parseInt($(this).closest('.vbmm-media-card').data('id'));
                var item = self.getItemById(id);
                if (item) {
                    self.copyToClipboard(item.url);
                }
            });

            $(document).on('click', '.vbmm-media-card', function (e) {
                if ($(e.target).is('input[type="checkbox"]') || $(e.target).closest('.vbmm-card-action').length) {
                    return;
                }
                var id = parseInt($(this).data('id'));
                var cb = $(this).find('.vbmm-card-checkbox');
                cb.prop('checked', !cb.is(':checked')).trigger('change');
                self.toggleSelect(id, cb.is(':checked'));
            });

            // Export option tabs
            $(document).on('click', '.vbmm-export-option', function () {
                $('.vbmm-export-option').removeClass('active');
                $(this).addClass('active');
                var format = $(this).data('format');
                self.updateExportCode(format);
            });

            // Keyboard shortcut: Escape to close panels
            $(document).on('keydown', function (e) {
                if (e.key === 'Escape') {
                    $('#vbmm-export-modal').hide();
                    self.closeEditPanel();
                }
            });
        },

        /**
         * Get filter parameters
         */
        getFilterParams: function () {
            var sortVal = $('#vbmm-sort').val().split('-');
            return {
                search: $('#vbmm-search').val(),
                type: $('#vbmm-filter-type').val(),
                date: $('#vbmm-filter-date').val(),
                size: $('#vbmm-filter-size').val(),
                attached: $('#vbmm-filter-attached').val(),
                orderby: sortVal[0] || 'date',
                order: (sortVal[1] || 'desc').toUpperCase(),
                page: this.currentPage,
                per_page: 40,
            };
        },

        /**
         * Load media items via REST API
         */
        loadMedia: function (append) {
            var self = this;
            var params = this.getFilterParams();

            if (!append) {
                $('#vbmm-loading').show();
                $('#vbmm-media-grid').empty();
                $('#vbmm-no-results').hide();
            }

            $.ajax({
                url: vbmmData.restUrl + 'media',
                method: 'GET',
                data: params,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-WP-Nonce', vbmmData.restNonce);
                },
                success: function (response) {
                    $('#vbmm-loading').hide();

                    if (append) {
                        self.items = self.items.concat(response.items);
                    } else {
                        self.items = response.items;
                    }

                    self.totalItems = response.total;
                    self.totalPages = response.total_pages;

                    if (self.items.length === 0) {
                        $('#vbmm-no-results').show();
                    } else {
                        self.renderItems(response.items, append);
                    }

                    // Load more button
                    if (self.currentPage < self.totalPages) {
                        $('#vbmm-load-more').show();
                    } else {
                        $('#vbmm-load-more').hide();
                    }

                    self.updateSelectionUI();
                },
                error: function () {
                    $('#vbmm-loading').hide();
                    self.showToast(vbmmData.i18n.error, 'error');
                }
            });
        },

        /**
         * Load media library stats
         */
        loadStats: function () {
            $.ajax({
                url: vbmmData.restUrl + 'stats',
                method: 'GET',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-WP-Nonce', vbmmData.restNonce);
                },
                success: function (response) {
                    $('#vbmm-stat-total').text(response.total);
                    $('#vbmm-stat-size').text(response.total_size_hr);
                    if (vbmmData.shortpixelActive) {
                        $('#vbmm-stat-optimized').text(response.optimized);
                        $('.vbmm-stat-shortpixel').show();
                    }
                }
            });
        },

        /**
         * Render media items
         */
        renderItems: function (items, append) {
            var self = this;
            var $grid = $('#vbmm-media-grid');

            if (!append) {
                $grid.empty();
            }

            items.forEach(function (item) {
                var card = self.createCard(item);
                $grid.append(card);
            });

            // Apply current view
            if (self.currentView === 'list') {
                $grid.addClass('vbmm-view-list');
            }
        },

        /**
         * Create a media card element
         */
        createCard: function (item) {
            var isSelected = this.selectedIds.indexOf(item.id) > -1;
            var thumbUrl = item.medium || item.thumbnail || item.url;
            var ext = item.mime_type.split('/')[1] || '';
            if (ext === 'jpeg') ext = 'jpg';
            if (ext === 'svg+xml') ext = 'svg';

            var dimensions = '';
            if (item.width && item.height) {
                dimensions = item.width + '×' + item.height;
            }

            // ShortPixel badge
            var spBadge = '';
            if (vbmmData.shortpixelActive) {
                if (item.shortpixel_status === 2) {
                    spBadge = '<span class="vbmm-card-sp-badge optimized" title="' + vbmmData.i18n.optimized + '">✓</span>';
                } else {
                    spBadge = '<span class="vbmm-card-sp-badge not-optimized" title="' + vbmmData.i18n.notOptimized + '">!</span>';
                }
            }

            var html = '<div class="vbmm-media-card' + (isSelected ? ' selected' : '') + '" data-id="' + item.id + '">' +
                '<input type="checkbox" class="vbmm-card-checkbox"' + (isSelected ? ' checked' : '') + '>' +
                '<div class="vbmm-card-thumb">' +
                    '<img src="' + this.escHtml(thumbUrl) + '" alt="' + this.escHtml(item.alt || item.title) + '" loading="lazy">' +
                    '<span class="vbmm-card-type-badge">' + this.escHtml(ext.toUpperCase()) + '</span>' +
                    spBadge +
                '</div>' +
                '<div class="vbmm-card-info">' +
                    '<div class="vbmm-card-title" title="' + this.escHtml(item.title) + '">' + this.escHtml(item.title) + '</div>' +
                    '<div class="vbmm-card-meta">' +
                        '<span>' + this.escHtml(item.filesize) + '</span>' +
                        '<span>' + this.escHtml(dimensions) + '</span>' +
                    '</div>';

            // List view extras
            if (this.currentView === 'list') {
                html += '<span class="vbmm-card-list-url" title="' + this.escHtml(item.url) + '">' + this.escHtml(item.url) + '</span>';
                if (item.alt) {
                    html += '<span class="vbmm-card-list-alt" title="' + this.escHtml(item.alt) + '">alt: ' + this.escHtml(item.alt) + '</span>';
                }
            }

            html += '</div>' +
                '<div class="vbmm-card-actions">' +
                    '<button type="button" class="vbmm-card-action" data-action="edit" title="Szerkesztés"><span class="dashicons dashicons-edit"></span></button>' +
                    '<button type="button" class="vbmm-card-action" data-action="copy" title="URL másolása"><span class="dashicons dashicons-clipboard"></span></button>' +
                '</div>' +
            '</div>';

            return html;
        },

        /**
         * Set view mode
         */
        setView: function (view) {
            this.currentView = view;
            $('.vbmm-view-btn').removeClass('active');
            $('.vbmm-view-btn[data-view="' + view + '"]').addClass('active');

            var $grid = $('#vbmm-media-grid');
            if (view === 'list') {
                $grid.addClass('vbmm-view-list');
            } else {
                $grid.removeClass('vbmm-view-list');
            }

            // Re-render for list-specific details
            this.renderItems(this.items, false);
        },

        /**
         * Toggle selection of a single item
         */
        toggleSelect: function (id, selected) {
            var idx = this.selectedIds.indexOf(id);
            if (selected && idx === -1) {
                this.selectedIds.push(id);
            } else if (!selected && idx > -1) {
                this.selectedIds.splice(idx, 1);
            }

            var $card = $('.vbmm-media-card[data-id="' + id + '"]');
            if (selected) {
                $card.addClass('selected');
            } else {
                $card.removeClass('selected');
            }

            this.updateSelectionUI();
        },

        /**
         * Toggle select all visible items
         */
        toggleSelectAll: function (selectAll) {
            var self = this;
            this.selectedIds = [];

            if (selectAll) {
                this.items.forEach(function (item) {
                    self.selectedIds.push(item.id);
                });
            }

            $('.vbmm-media-card').each(function () {
                var $card = $(this);
                if (selectAll) {
                    $card.addClass('selected').find('.vbmm-card-checkbox').prop('checked', true);
                } else {
                    $card.removeClass('selected').find('.vbmm-card-checkbox').prop('checked', false);
                }
            });

            this.updateSelectionUI();
        },

        /**
         * Update selection-related UI elements
         */
        updateSelectionUI: function () {
            var count = this.selectedIds.length;

            if (count > 0) {
                $('#vbmm-selected-count').show();
                $('#vbmm-count-number').text(count);
                $('#vbmm-bulk-bar').show();
                $('#vbmm-bulk-count').text(count);
            } else {
                $('#vbmm-selected-count').hide();
                $('#vbmm-bulk-bar').hide();
            }

            // Update select all checkbox state
            if (this.items.length > 0 && count === this.items.length) {
                $('#vbmm-select-all').prop('checked', true);
            } else {
                $('#vbmm-select-all').prop('checked', false);
            }
        },

        /**
         * Get selected items
         */
        getSelectedItems: function () {
            var self = this;
            return this.selectedIds.map(function (id) {
                return self.getItemById(id);
            }).filter(Boolean);
        },

        /**
         * Get item by ID
         */
        getItemById: function (id) {
            for (var i = 0; i < this.items.length; i++) {
                if (this.items[i].id === id) {
                    return this.items[i];
                }
            }
            return null;
        },

        /**
         * Show export modal with formatted code
         */
        showExportModal: function (format) {
            var selected = this.getSelectedItems();
            if (selected.length === 0) return;

            // Build format tabs
            var formats = [
                { key: 'html', label: 'HTML &lt;img&gt;' },
                { key: 'html-figure', label: 'HTML &lt;figure&gt;' },
                { key: 'html-picture', label: 'HTML &lt;picture&gt;' },
                { key: 'urls', label: 'URL lista' },
                { key: 'markdown', label: 'Markdown' },
                { key: 'css', label: 'CSS background' },
                { key: 'array', label: 'JS/PHP Array' },
                { key: 'csv', label: 'CSV' },
                { key: 'json', label: 'JSON' },
                { key: 'claude', label: 'Claude prompt' },
            ];

            var optionsHtml = '';
            formats.forEach(function (f) {
                var active = f.key === format ? ' active' : '';
                optionsHtml += '<button type="button" class="vbmm-export-option' + active + '" data-format="' + f.key + '">' + f.label + '</button>';
            });

            $('#vbmm-export-options').html(optionsHtml);
            this.updateExportCode(format);
            $('#vbmm-export-modal').show();
        },

        /**
         * Generate export code for selected format
         */
        updateExportCode: function (format) {
            var selected = this.getSelectedItems();
            var code = '';

            switch (format) {
                case 'html':
                    code = this.exportHtml(selected);
                    break;
                case 'html-figure':
                    code = this.exportHtmlFigure(selected);
                    break;
                case 'html-picture':
                    code = this.exportHtmlPicture(selected);
                    break;
                case 'urls':
                    code = this.exportUrls(selected);
                    break;
                case 'markdown':
                    code = this.exportMarkdown(selected);
                    break;
                case 'css':
                    code = this.exportCss(selected);
                    break;
                case 'array':
                    code = this.exportArray(selected);
                    break;
                case 'csv':
                    code = this.exportCsv(selected);
                    break;
                case 'json':
                    code = this.exportJson(selected);
                    break;
                case 'claude':
                    code = this.exportClaude(selected);
                    break;
            }

            $('#vbmm-export-code').val(code);
            this._currentFormat = format;
        },

        /**
         * Export formats
         */
        exportHtml: function (items) {
            return items.map(function (item) {
                var attrs = 'src="' + item.url + '"';
                attrs += ' alt="' + (item.alt || item.title) + '"';
                if (item.width && item.height) {
                    attrs += ' width="' + item.width + '" height="' + item.height + '"';
                }
                attrs += ' loading="lazy"';
                return '<img ' + attrs + '>';
            }).join('\n');
        },

        exportHtmlFigure: function (items) {
            return items.map(function (item) {
                var html = '<figure>\n';
                html += '  <img src="' + item.url + '"';
                html += ' alt="' + (item.alt || item.title) + '"';
                if (item.width && item.height) {
                    html += ' width="' + item.width + '" height="' + item.height + '"';
                }
                html += ' loading="lazy">\n';
                if (item.caption) {
                    html += '  <figcaption>' + item.caption + '</figcaption>\n';
                }
                html += '</figure>';
                return html;
            }).join('\n\n');
        },

        exportHtmlPicture: function (items) {
            return items.map(function (item) {
                var html = '<picture>\n';
                // WebP source if different format
                if (item.mime_type !== 'image/webp') {
                    var webpUrl = item.url.replace(/\.(jpg|jpeg|png)$/i, '.webp');
                    html += '  <source srcset="' + webpUrl + '" type="image/webp">\n';
                }
                html += '  <img src="' + item.url + '"';
                html += ' alt="' + (item.alt || item.title) + '"';
                if (item.width && item.height) {
                    html += ' width="' + item.width + '" height="' + item.height + '"';
                }
                html += ' loading="lazy">\n';
                html += '</picture>';
                return html;
            }).join('\n\n');
        },

        exportUrls: function (items) {
            return items.map(function (item) {
                return item.url;
            }).join('\n');
        },

        exportMarkdown: function (items) {
            return items.map(function (item) {
                return '![' + (item.alt || item.title) + '](' + item.url + ')';
            }).join('\n');
        },

        exportCss: function (items) {
            return items.map(function (item, index) {
                var className = item.title.replace(/[^a-zA-Z0-9-]/g, '-').toLowerCase();
                return '.bg-' + className + ' {\n' +
                    '  background-image: url(\'' + item.url + '\');\n' +
                    '  background-size: cover;\n' +
                    '  background-position: center;\n' +
                    '}';
            }).join('\n\n');
        },

        exportArray: function (items) {
            var jsArray = 'const images = [\n' +
                items.map(function (item) {
                    return '  {\n' +
                        '    id: ' + item.id + ',\n' +
                        '    url: \'' + item.url + '\',\n' +
                        '    alt: \'' + (item.alt || '').replace(/'/g, "\\'") + '\',\n' +
                        '    title: \'' + item.title.replace(/'/g, "\\'") + '\',\n' +
                        (item.width ? '    width: ' + item.width + ',\n' : '') +
                        (item.height ? '    height: ' + item.height + ',\n' : '') +
                        '  }';
                }).join(',\n') + '\n];\n\n';

            var phpArray = '$images = [\n' +
                items.map(function (item) {
                    return '  [\n' +
                        '    \'id\'    => ' + item.id + ',\n' +
                        '    \'url\'   => \'' + item.url + '\',\n' +
                        '    \'alt\'   => \'' + (item.alt || '').replace(/'/g, "\\'") + '\',\n' +
                        '    \'title\' => \'' + item.title.replace(/'/g, "\\'") + '\',\n' +
                        '  ]';
                }).join(',\n') + '\n];';

            return '// JavaScript\n' + jsArray + '// PHP\n' + phpArray;
        },

        exportCsv: function (items) {
            var header = 'ID,Title,Alt Text,URL,MIME Type,Width,Height,File Size';
            var rows = items.map(function (item) {
                return [
                    item.id,
                    '"' + (item.title || '').replace(/"/g, '""') + '"',
                    '"' + (item.alt || '').replace(/"/g, '""') + '"',
                    item.url,
                    item.mime_type,
                    item.width || '',
                    item.height || '',
                    item.filesize
                ].join(',');
            });
            return header + '\n' + rows.join('\n');
        },

        exportJson: function (items) {
            var data = items.map(function (item) {
                return {
                    id: item.id,
                    title: item.title,
                    alt: item.alt || '',
                    url: item.url,
                    mime_type: item.mime_type,
                    width: item.width || null,
                    height: item.height || null,
                    filesize: item.filesize,
                };
            });
            return JSON.stringify(data, null, 2);
        },

        exportClaude: function (items) {
            var lines = [
                'Az alábbi képek állnak rendelkezésre a VanBudapest weboldalról:',
                '',
            ];

            items.forEach(function (item, i) {
                lines.push((i + 1) + '. **' + item.title + '**');
                lines.push('   - URL: `' + item.url + '`');
                if (item.alt) {
                    lines.push('   - Alt: "' + item.alt + '"');
                }
                if (item.width && item.height) {
                    lines.push('   - Méret: ' + item.width + '×' + item.height + 'px');
                }
                lines.push('   - Formátum: ' + item.mime_type.split('/')[1].toUpperCase());
                lines.push('');
            });

            lines.push('Kérlek használd ezeket a képeket a HTML kódban az `<img>` tageknél a megfelelő `src`, `alt`, `width` és `height` attribútumokkal.');

            return lines.join('\n');
        },

        /**
         * Open inline edit panel for a media item
         */
        openEditPanel: function (id) {
            var self = this;

            $.ajax({
                url: vbmmData.restUrl + 'media/' + id,
                method: 'GET',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-WP-Nonce', vbmmData.restNonce);
                },
                success: function (item) {
                    $('#vbmm-edit-id').val(item.id);
                    $('#vbmm-edit-preview-img').attr('src', item.medium || item.url);
                    $('#vbmm-edit-title').val(item.title);
                    $('#vbmm-edit-alt').val(item.alt);
                    $('#vbmm-edit-caption').val(item.caption);
                    $('#vbmm-edit-description').val(item.description);
                    $('#vbmm-edit-url').val(item.url);
                    $('#vbmm-edit-filesize').text(item.filesize);
                    $('#vbmm-edit-date').text(self.formatDate(item.date));

                    if (item.width && item.height) {
                        $('#vbmm-edit-dimensions').text(item.width + ' × ' + item.height + ' px');
                    } else {
                        $('#vbmm-edit-dimensions').text('-');
                    }

                    // Edit link
                    if (item.edit_link) {
                        $('#vbmm-edit-wp-link').attr('href', item.edit_link).show();
                    } else {
                        $('#vbmm-edit-wp-link').hide();
                    }

                    // Available sizes
                    if (item.sizes) {
                        var sizesHtml = '';
                        Object.keys(item.sizes).forEach(function (name) {
                            var size = item.sizes[name];
                            sizesHtml += '<div class="vbmm-size-item">' +
                                '<span class="vbmm-size-name">' + self.escHtml(name) + '</span>' +
                                '<span class="vbmm-size-dims">' + size.width + '×' + size.height + '</span>' +
                                '<a href="#" class="vbmm-size-copy" data-url="' + self.escHtml(size.url) + '">URL másolása</a>' +
                            '</div>';
                        });
                        $('#vbmm-sizes-list').html(sizesHtml);
                        $('#vbmm-edit-sizes').show();
                    } else {
                        $('#vbmm-edit-sizes').hide();
                    }

                    $('#vbmm-edit-panel').show();
                }
            });
        },

        /**
         * Close edit panel
         */
        closeEditPanel: function () {
            $('#vbmm-edit-panel').hide();
        },

        /**
         * Save inline edit
         */
        saveEdit: function () {
            var self = this;
            var id = parseInt($('#vbmm-edit-id').val());

            var data = {
                title: $('#vbmm-edit-title').val(),
                alt: $('#vbmm-edit-alt').val(),
                caption: $('#vbmm-edit-caption').val(),
                description: $('#vbmm-edit-description').val(),
            };

            $.ajax({
                url: vbmmData.restUrl + 'media/' + id,
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-WP-Nonce', vbmmData.restNonce);
                },
                success: function (item) {
                    // Update local cache
                    for (var i = 0; i < self.items.length; i++) {
                        if (self.items[i].id === id) {
                            self.items[i].title = item.title;
                            self.items[i].alt = item.alt;
                            self.items[i].caption = item.caption;
                            self.items[i].description = item.description;
                            break;
                        }
                    }

                    // Update card in DOM
                    var $card = $('.vbmm-media-card[data-id="' + id + '"]');
                    $card.find('.vbmm-card-title').text(item.title).attr('title', item.title);

                    self.showToast(vbmmData.i18n.saved, 'success');
                },
                error: function () {
                    self.showToast(vbmmData.i18n.error, 'error');
                }
            });
        },

        /**
         * Bulk delete selected items
         */
        bulkDelete: function () {
            var self = this;
            if (this.selectedIds.length === 0) return;

            if (!confirm(vbmmData.i18n.deleteConfirm)) return;

            $.ajax({
                url: vbmmData.restUrl + 'media/bulk-delete',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ ids: this.selectedIds }),
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-WP-Nonce', vbmmData.restNonce);
                },
                success: function (response) {
                    // Remove deleted items from DOM and cache
                    response.deleted.forEach(function (id) {
                        $('.vbmm-media-card[data-id="' + id + '"]').fadeOut(300, function () {
                            $(this).remove();
                        });
                        self.items = self.items.filter(function (item) {
                            return item.id !== id;
                        });
                    });

                    self.selectedIds = [];
                    self.updateSelectionUI();
                    self.loadStats();

                    var msg = response.deleted.length + ' fájl törölve.';
                    if (response.failed.length > 0) {
                        msg += ' ' + response.failed.length + ' nem sikerült.';
                    }
                    self.showToast(msg, response.failed.length > 0 ? 'error' : 'success');
                },
                error: function () {
                    self.showToast(vbmmData.i18n.error, 'error');
                }
            });
        },

        /**
         * Bulk optimize via ShortPixel
         */
        bulkOptimize: function () {
            var self = this;
            if (this.selectedIds.length === 0) return;

            if (!vbmmData.shortpixelActive) {
                self.showToast('ShortPixel plugin nincs aktiválva.', 'error');
                return;
            }

            $.ajax({
                url: vbmmData.restUrl + 'shortpixel/optimize',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ ids: this.selectedIds }),
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-WP-Nonce', vbmmData.restNonce);
                },
                success: function (response) {
                    self.showToast(response.message, 'success');
                },
                error: function () {
                    self.showToast(vbmmData.i18n.error, 'error');
                }
            });
        },

        /**
         * Copy text to clipboard
         */
        copyToClipboard: function (text) {
            var self = this;
            if (navigator.clipboard) {
                navigator.clipboard.writeText(text).then(function () {
                    self.showToast(vbmmData.i18n.copied, 'success');
                });
            } else {
                // Fallback
                var $temp = $('<textarea>').val(text).appendTo('body').select();
                document.execCommand('copy');
                $temp.remove();
                self.showToast(vbmmData.i18n.copied, 'success');
            }
        },

        /**
         * Download export as file
         */
        downloadExport: function () {
            var code = $('#vbmm-export-code').val();
            var format = this._currentFormat || 'txt';
            var ext = 'txt';
            var mime = 'text/plain';

            switch (format) {
                case 'html':
                case 'html-figure':
                case 'html-picture':
                    ext = 'html';
                    mime = 'text/html';
                    break;
                case 'css':
                    ext = 'css';
                    mime = 'text/css';
                    break;
                case 'csv':
                    ext = 'csv';
                    mime = 'text/csv';
                    break;
                case 'json':
                    ext = 'json';
                    mime = 'application/json';
                    break;
                case 'markdown':
                case 'claude':
                    ext = 'md';
                    break;
                case 'array':
                    ext = 'js';
                    mime = 'text/javascript';
                    break;
            }

            var blob = new Blob([code], { type: mime + ';charset=utf-8' });
            var link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'vanbudapest-media-export.' + ext;
            link.click();
            URL.revokeObjectURL(link.href);
        },

        /**
         * Show toast notification
         */
        showToast: function (message, type) {
            var icon = type === 'success' ? 'yes-alt' : (type === 'error' ? 'warning' : 'info-outline');
            var $toast = $('<div class="vbmm-toast ' + (type || '') + '">' +
                '<span class="dashicons dashicons-' + icon + '"></span>' +
                message +
            '</div>');

            $('body').append($toast);

            setTimeout(function () {
                $toast.fadeOut(300, function () {
                    $(this).remove();
                });
            }, 3000);
        },

        /**
         * Format date string
         */
        formatDate: function (dateStr) {
            var d = new Date(dateStr);
            return d.getFullYear() + '.' +
                String(d.getMonth() + 1).padStart(2, '0') + '.' +
                String(d.getDate()).padStart(2, '0') + '. ' +
                String(d.getHours()).padStart(2, '0') + ':' +
                String(d.getMinutes()).padStart(2, '0');
        },

        /**
         * HTML escape
         */
        escHtml: function (str) {
            if (!str) return '';
            var div = document.createElement('div');
            div.textContent = str;
            return div.innerHTML;
        }
    };

    // Initialize when DOM ready
    $(document).ready(function () {
        if ($('.vbmm-wrap').length) {
            VBMM.init();
        }
    });

})(jQuery);
