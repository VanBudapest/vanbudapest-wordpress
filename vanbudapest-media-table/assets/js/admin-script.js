/**
 * VanBudapest Média Táblázat - Admin JavaScript
 */

(function($) {
    'use strict';

    // State management
    const state = {
        currentPage: 1,
        totalPages: 1,
        totalItems: 0,
        currentFilter: 'all',
        searchQuery: '',
        perPage: 50,
        sortField: 'date',
        sortOrder: 'desc',
        mediaItems: []
    };

    // Category labels
    const categoryLabels = {
        'f1': 'F1',
        'airport': 'Reptér',
        'fleet': 'Flotta',
        'balaton': 'Balaton',
        'budapest': 'Budapest',
        'festival': 'Fesztivál',
        'vip': 'VIP',
        'other': 'Egyéb'
    };

    // File type icons
    const fileIcons = {
        'video': '🎬',
        'audio': '🎵',
        'application/pdf': '📄',
        'default': '📁'
    };

    // Initialize
    $(document).ready(function() {
        loadMedia();
        bindEvents();
    });

    // Bind event handlers
    function bindEvents() {
        // Filter buttons
        $('.vbmt-filter-btn').on('click', function() {
            $('.vbmt-filter-btn').removeClass('active');
            $(this).addClass('active');
            state.currentFilter = $(this).data('filter');
            state.currentPage = 1;
            loadMedia();
        });

        // Search input with debounce
        let searchTimeout;
        $('#vbmt-search').on('input', function() {
            clearTimeout(searchTimeout);
            const query = $(this).val();
            searchTimeout = setTimeout(function() {
                state.searchQuery = query;
                state.currentPage = 1;
                loadMedia();
            }, 300);
        });

        // Pagination
        $('#vbmt-prev-page').on('click', function() {
            if (state.currentPage > 1) {
                state.currentPage--;
                loadMedia();
            }
        });

        $('#vbmt-next-page').on('click', function() {
            if (state.currentPage < state.totalPages) {
                state.currentPage++;
                loadMedia();
            }
        });

        // Sortable columns
        $('.vbmt-sortable').on('click', function() {
            const field = $(this).data('sort');
            if (state.sortField === field) {
                state.sortOrder = state.sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                state.sortField = field;
                state.sortOrder = 'asc';
            }
            sortAndRenderTable();
        });

        // Modal close
        $('#vbmt-modal-close, #vbmt-modal').on('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });

        // ESC key to close modal
        $(document).on('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });

        // Modal copy button
        $('#vbmt-modal-copy').on('click', function() {
            const url = $('#vbmt-modal-url').val();
            copyToClipboard(url, $(this));
        });
    }

    // Load media from server
    function loadMedia() {
        const $tableBody = $('#vbmt-table-body');
        $tableBody.html('<tr><td colspan="5" class="vbmt-loading">⏳ Betöltés...</td></tr>');

        $.ajax({
            url: vbmt_ajax.ajax_url,
            type: 'POST',
            data: {
                action: 'vbmt_get_media',
                nonce: vbmt_ajax.nonce,
                page: state.currentPage,
                per_page: state.perPage,
                category: state.currentFilter,
                search: state.searchQuery
            },
            success: function(response) {
                if (response.success) {
                    state.mediaItems = response.data.items;
                    state.totalItems = response.data.total;
                    state.totalPages = response.data.pages;
                    state.currentPage = response.data.current_page;

                    sortAndRenderTable();
                    updateStats();
                    updatePagination();
                } else {
                    $tableBody.html('<tr><td colspan="5" class="vbmt-loading">❌ Hiba: ' + response.data + '</td></tr>');
                }
            },
            error: function() {
                $tableBody.html('<tr><td colspan="5" class="vbmt-loading">❌ Hálózati hiba történt</td></tr>');
            }
        });
    }

    // Sort and render table
    function sortAndRenderTable() {
        const sorted = [...state.mediaItems].sort((a, b) => {
            let valA = a[state.sortField] || '';
            let valB = b[state.sortField] || '';

            if (state.sortField === 'date') {
                valA = new Date(valA);
                valB = new Date(valB);
            }

            if (valA < valB) return state.sortOrder === 'asc' ? -1 : 1;
            if (valA > valB) return state.sortOrder === 'asc' ? 1 : -1;
            return 0;
        });

        renderTable(sorted);
    }

    // Render table
    function renderTable(items) {
        const $tableBody = $('#vbmt-table-body');

        if (items.length === 0) {
            $tableBody.html('<tr><td colspan="5" class="vbmt-loading">Nincs találat</td></tr>');
            return;
        }

        let html = '';
        items.forEach(function(item) {
            const categoryClass = 'vbmt-cat-' + item.category;
            const categoryLabel = categoryLabels[item.category] || 'Egyéb';

            let thumbnailHtml;
            if (item.is_image && item.thumb_url) {
                thumbnailHtml = '<img src="' + escapeHtml(item.thumb_url) + '" ' +
                    'alt="' + escapeHtml(item.title) + '" ' +
                    'class="vbmt-thumb" ' +
                    'data-full-url="' + escapeHtml(item.url) + '" ' +
                    'data-title="' + escapeHtml(item.title) + '">';
            } else {
                const icon = getFileIcon(item.mime_type);
                thumbnailHtml = '<div class="vbmt-non-image">' + icon + '</div>';
            }

            html += '<tr data-id="' + item.id + '">' +
                '<td>' + escapeHtml(item.date) + '</td>' +
                '<td>' + thumbnailHtml + '</td>' +
                '<td class="vbmt-title-cell" title="' + escapeHtml(item.title) + '">' + escapeHtml(item.title) + '</td>' +
                '<td class="vbmt-url-display">' +
                    '<button class="vbmt-copy-btn" data-url="' + escapeHtml(item.url) + '">📋 Másolás</button>' +
                    '<span class="vbmt-url-text">' + escapeHtml(item.url) + '</span>' +
                '</td>' +
                '<td><span class="vbmt-category-badge ' + categoryClass + '">' + categoryLabel + '</span></td>' +
                '</tr>';
        });

        $tableBody.html(html);

        // Bind copy buttons
        $tableBody.find('.vbmt-copy-btn').on('click', function(e) {
            e.stopPropagation();
            const url = $(this).data('url');
            copyToClipboard(url, $(this));
        });

        // Bind thumbnail click for modal
        $tableBody.find('.vbmt-thumb').on('click', function() {
            openModal($(this).data('full-url'), $(this).data('title'));
        });
    }

    // Get file icon based on mime type
    function getFileIcon(mimeType) {
        if (mimeType.startsWith('video/')) return fileIcons['video'];
        if (mimeType.startsWith('audio/')) return fileIcons['audio'];
        if (mimeType === 'application/pdf') return fileIcons['application/pdf'];
        return fileIcons['default'];
    }

    // Update statistics display
    function updateStats() {
        $('#vbmt-visible-count').text(state.mediaItems.length);
        $('#vbmt-total-count').text(state.totalItems);
    }

    // Update pagination controls
    function updatePagination() {
        $('#vbmt-current-page').text(state.currentPage);
        $('#vbmt-total-pages').text(state.totalPages);

        $('#vbmt-prev-page').prop('disabled', state.currentPage <= 1);
        $('#vbmt-next-page').prop('disabled', state.currentPage >= state.totalPages);
    }

    // Copy to clipboard
    function copyToClipboard(text, $button) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(function() {
                showCopySuccess($button);
            }).catch(function() {
                fallbackCopy(text, $button);
            });
        } else {
            fallbackCopy(text, $button);
        }
    }

    // Fallback copy method
    function fallbackCopy(text, $button) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();

        try {
            document.execCommand('copy');
            showCopySuccess($button);
        } catch (err) {
            showToast('Másolás sikertelen!');
        }

        document.body.removeChild(textarea);
    }

    // Show copy success feedback
    function showCopySuccess($button) {
        const originalText = $button.text();
        $button.addClass('copied').text('✓ Másolva!');
        showToast('Link vágólapra másolva!');

        setTimeout(function() {
            $button.removeClass('copied').text(originalText);
        }, 1500);
    }

    // Show toast notification
    function showToast(message) {
        const $toast = $('#vbmt-toast');
        $toast.text(message).addClass('show');

        setTimeout(function() {
            $toast.removeClass('show');
        }, 2000);
    }

    // Open modal
    function openModal(url, title) {
        const $modal = $('#vbmt-modal');
        $('#vbmt-modal-image').attr('src', url);
        $('#vbmt-modal-title').text(title);
        $('#vbmt-modal-url').val(url);
        $modal.addClass('active');
        $('body').css('overflow', 'hidden');
    }

    // Close modal
    function closeModal() {
        const $modal = $('#vbmt-modal');
        $modal.removeClass('active');
        $('body').css('overflow', '');
    }

    // Escape HTML
    function escapeHtml(text) {
        if (!text) return '';
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return String(text).replace(/[&<>"']/g, function(m) { return map[m]; });
    }

})(jQuery);
