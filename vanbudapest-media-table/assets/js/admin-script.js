/**
 * VanBudapest Média Táblázat - Excel-szerű admin script
 */

(function($) {
    'use strict';

    const state = {
        currentPage: 1,
        totalPages: 1,
        totalItems: 0,
        currentFilter: 'all',
        searchQuery: '',
        perPage: 500,
        sortField: 'date',
        sortOrder: 'desc',
        mediaItems: []
    };

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

    const fileIcons = {
        'video': '🎬',
        'audio': '🎵',
        'application/pdf': '📄',
        'default': '📁'
    };

    $(document).ready(function() {
        loadMedia();
        bindEvents();
    });

    function bindEvents() {
        // Kategória szűrő dropdown
        $('#vbmt-category-filter').on('change', function() {
            state.currentFilter = $(this).val();
            state.currentPage = 1;
            loadMedia();
        });

        // Keresés
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

        // Lapozás
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

        // Rendezés
        $('.vbmt-sortable').on('click', function() {
            const field = $(this).data('sort');
            if (state.sortField === field) {
                state.sortOrder = state.sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                state.sortField = field;
                state.sortOrder = 'desc';
            }
            updateSortIndicators();
            sortAndRenderTable();
        });

        // Modal bezárás
        $('#vbmt-modal-close, #vbmt-modal').on('click', function(e) {
            if (e.target === this || $(e.target).is('#vbmt-modal-close')) {
                closeModal();
            }
        });

        $(document).on('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });

        // Modal másolás gomb
        $('#vbmt-modal-copy').on('click', function() {
            const url = $('#vbmt-modal-url').val();
            copyToClipboard(url, $(this));
        });
    }

    function updateSortIndicators() {
        $('.vbmt-sortable').each(function() {
            const field = $(this).data('sort');
            let text = $(this).text().replace(' ▼', '').replace(' ▲', '');
            if (field === state.sortField) {
                text += state.sortOrder === 'desc' ? ' ▼' : ' ▲';
            }
            $(this).text(text);
        });
    }

    function loadMedia() {
        const $tableBody = $('#vbmt-table-body');
        $tableBody.html('<tr><td colspan="5" class="vbmt-loading">Betöltés...</td></tr>');

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
                    $tableBody.html('<tr><td colspan="5" class="vbmt-loading">Hiba: ' + response.data + '</td></tr>');
                }
            },
            error: function() {
                $tableBody.html('<tr><td colspan="5" class="vbmt-loading">Hálózati hiba</td></tr>');
            }
        });
    }

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
                '<td style="text-align:center">' + thumbnailHtml + '</td>' +
                '<td><div class="vbmt-link-cell" title="' + escapeHtml(item.url) + '">' + escapeHtml(item.url) + '</div></td>' +
                '<td style="text-align:center"><button class="vbmt-copy-btn" data-url="' + escapeHtml(item.url) + '">Másolás</button></td>' +
                '<td><span class="vbmt-category ' + categoryClass + '">' + categoryLabel + '</span></td>' +
                '</tr>';
        });

        $tableBody.html(html);

        // Másolás gombok
        $tableBody.find('.vbmt-copy-btn').on('click', function(e) {
            e.stopPropagation();
            const url = $(this).data('url');
            copyToClipboard(url, $(this));
        });

        // Link cellára kattintás - kijelölés
        $tableBody.find('.vbmt-link-cell').on('click', function() {
            selectText(this);
        });

        // Kép kattintás - modal
        $tableBody.find('.vbmt-thumb').on('click', function() {
            openModal($(this).data('full-url'), $(this).data('title'));
        });

        // Sor kiválasztás
        $tableBody.find('tr').on('click', function(e) {
            if (!$(e.target).is('.vbmt-copy-btn, .vbmt-thumb, .vbmt-link-cell')) {
                $tableBody.find('tr').removeClass('selected');
                $(this).addClass('selected');
            }
        });
    }

    function selectText(element) {
        const range = document.createRange();
        range.selectNodeContents(element);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
    }

    function getFileIcon(mimeType) {
        if (!mimeType) return fileIcons['default'];
        if (mimeType.startsWith('video/')) return fileIcons['video'];
        if (mimeType.startsWith('audio/')) return fileIcons['audio'];
        if (mimeType === 'application/pdf') return fileIcons['application/pdf'];
        return fileIcons['default'];
    }

    function updateStats() {
        $('#vbmt-visible-count').text(state.mediaItems.length);
        $('#vbmt-total-count').text(state.totalItems);
    }

    function updatePagination() {
        $('#vbmt-current-page').text(state.currentPage);
        $('#vbmt-total-pages').text(state.totalPages || 1);

        $('#vbmt-prev-page').prop('disabled', state.currentPage <= 1);
        $('#vbmt-next-page').prop('disabled', state.currentPage >= state.totalPages);
    }

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

    function showCopySuccess($button) {
        const originalText = $button.text();
        $button.addClass('copied').text('✓ OK');
        showToast('Link vágólapra másolva!');

        setTimeout(function() {
            $button.removeClass('copied').text(originalText);
        }, 1500);
    }

    function showToast(message) {
        const $toast = $('#vbmt-toast');
        $toast.text(message).addClass('show');

        setTimeout(function() {
            $toast.removeClass('show');
        }, 2000);
    }

    function openModal(url, title) {
        const $modal = $('#vbmt-modal');
        $('#vbmt-modal-image').attr('src', url);
        $('#vbmt-modal-url').val(url);
        $modal.addClass('active');
        $('body').css('overflow', 'hidden');
    }

    function closeModal() {
        const $modal = $('#vbmt-modal');
        $modal.removeClass('active');
        $('body').css('overflow', '');
    }

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
