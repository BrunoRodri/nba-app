/**
 * NBA Stats Explorer — Main JavaScript
 * Dark mode toggle, search UX, and micro-interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initSearchFocus();
    initAnimations();
    initAutocomplete();
});





// ─── Mobile Menu ─────────────────────────────────────────────────────

function initMobileMenu() {
    const btn = document.getElementById('mobile-menu-btn');
    const search = document.getElementById('mobile-search');
    if (!btn || !search) return;

    btn.addEventListener('click', () => {
        search.classList.toggle('hidden');
        // Focus the input when opening
        if (!search.classList.contains('hidden')) {
            const input = document.getElementById('mobile-search-input');
            if (input) input.focus();
        }
    });
}


// ─── Search Focus ────────────────────────────────────────────────────

function initSearchFocus() {
    // Keyboard shortcut: "/" to focus search
    document.addEventListener('keydown', (e) => {
        if (e.key === '/' && !isInputFocused()) {
            e.preventDefault();
            const input = document.getElementById('nav-search-input') ||
                          document.getElementById('hero-search-input');
            if (input) {
                input.focus();
                input.select();
            }
        }
    });
}

function isInputFocused() {
    const active = document.activeElement;
    return active && (
        active.tagName === 'INPUT' ||
        active.tagName === 'TEXTAREA' ||
        active.isContentEditable
    );
}


// ─── Scroll Animations ──────────────────────────────────────────────

function initAnimations() {
    // Intersection Observer for fade-in animations
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px',
        }
    );

    // Observe elements with animation classes
    document.querySelectorAll('.animate-fade-in, .animate-slide-up').forEach((el) => {
        // Set initial state for scroll-triggered animations
        if (!isInViewport(el)) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(el);
        }
    });
}

function isInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top < window.innerHeight &&
        rect.bottom > 0
    );
}


// ─── Autocomplete ───────────────────────────────────────────────────

function initAutocomplete() {
    const inputs = [
        { inputId: 'nav-search-input', dropdownId: 'nav-search-suggestions' },
        { inputId: 'hero-search-input', dropdownId: 'hero-search-suggestions' },
        { inputId: 'mobile-search-input', dropdownId: 'mobile-search-suggestions' }
    ];

    inputs.forEach(({ inputId, dropdownId }) => {
        const input = document.getElementById(inputId);
        const dropdown = document.getElementById(dropdownId);
        
        if (!input || !dropdown) return;

        let timeout = null;

        // Hide dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!input.contains(e.target) && !dropdown.contains(e.target)) {
                hideDropdown(dropdown);
            }
        });

        // Show dropdown on focus if there's text
        input.addEventListener('focus', () => {
            if (input.value.trim().length >= 2) {
                fetchSuggestions(input.value.trim(), dropdown);
            }
        });

        // Handle typing
        input.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            
            clearTimeout(timeout);
            
            if (query.length < 2) {
                hideDropdown(dropdown);
                return;
            }

            timeout = setTimeout(() => {
                fetchSuggestions(query, dropdown);
            }, 300); // Debounce 300ms
        });
    });
}

async function fetchSuggestions(query, dropdown) {
    try {
        const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        renderSuggestions(data, dropdown);
    } catch (error) {
        console.error('Error fetching suggestions:', error);
        hideDropdown(dropdown);
    }
}

function renderSuggestions(data, dropdown) {
    const { players, teams } = data;
    
    if (players.length === 0 && teams.length === 0) {
        dropdown.innerHTML = `
            <div class="p-4 text-center text-sm text-slate-500">
                Nenhum resultado encontrado.
            </div>
        `;
    } else {
        let html = '';
        
        if (players.length > 0) {
            html += `<div class="px-4 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider bg-slate-100 dark:bg-slate-900">Jogadores</div>`;
            players.forEach(p => {
                const status = p.is_active 
                    ? '<span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>' 
                    : '';
                html += `
                    <a href="${p.url}" class="flex items-center gap-3 px-4 py-3 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors border-b border-slate-100 dark:border-slate-700 last:border-0">
                        <div class="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 flex-shrink-0 overflow-hidden">
                            <img src="https://cdn.nba.com/headshots/nba/latest/1040x760/${p.id}.png" class="w-full h-full object-cover" onerror="this.style.display='none'">
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="text-sm font-medium text-slate-800 dark:text-slate-200 truncate">${p.name}</div>
                            <div class="flex items-center gap-1.5 mt-0.5">${status}</div>
                        </div>
                    </a>
                `;
            });
        }
        
        if (teams.length > 0) {
            html += `<div class="px-4 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider bg-slate-100 dark:bg-slate-900">Times</div>`;
            teams.forEach(t => {
                html += `
                    <a href="${t.url}" class="flex items-center gap-3 px-4 py-3 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors border-b border-slate-100 dark:border-slate-700 last:border-0">
                        <div class="w-8 h-8 flex-shrink-0">
                            <img src="https://cdn.nba.com/logos/nba/${t.id}/global/L/logo.svg" class="w-full h-full object-contain">
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="text-sm font-medium text-slate-800 dark:text-slate-200 truncate">${t.name}</div>
                            <div class="text-xs text-slate-500 truncate">${t.city}</div>
                        </div>
                    </a>
                `;
            });
        }
        
        dropdown.innerHTML = html;
    }
    
    showDropdown(dropdown);
}

function showDropdown(dropdown) {
    dropdown.classList.remove('hidden');
    // small delay to allow display block to apply before opacity transition
    setTimeout(() => {
        dropdown.classList.remove('opacity-0');
    }, 10);
}

function hideDropdown(dropdown) {
    dropdown.classList.add('opacity-0');
    setTimeout(() => {
        dropdown.classList.add('hidden');
    }, 200); // match transition duration
}

/**
 * Global Tab Switcher
 * Used in Standings and other tabbed interfaces
 */
window.switchTab = function(tab) {
    console.log('Switching to tab:', tab);
    
    // Tab contents
    const standingsTab = document.getElementById('tab-standings');
    const bracketTab = document.getElementById('tab-bracket');
    
    // Buttons
    const btnStandings = document.getElementById('btn-standings');
    const btnBracket = document.getElementById('btn-bracket');

    if (!standingsTab || !bracketTab || !btnStandings || !btnBracket) return;

    if (tab === 'standings') {
        // Show Standings
        standingsTab.classList.remove('hidden');
        bracketTab.classList.add('hidden');
        
        // Highlight button
        btnStandings.classList.add('bg-white', 'dark:bg-slate-700', 'text-nba-blue', 'shadow-sm');
        btnStandings.classList.remove('text-slate-500', 'dark:text-slate-400');
        
        btnBracket.classList.remove('bg-white', 'dark:bg-slate-700', 'text-nba-blue', 'shadow-sm');
        btnBracket.classList.add('text-slate-500', 'dark:text-slate-400');
    } else {
        // Show Bracket
        standingsTab.classList.add('hidden');
        bracketTab.classList.remove('hidden');
        
        // Highlight button
        btnBracket.classList.add('bg-white', 'dark:bg-slate-700', 'text-nba-blue', 'shadow-sm');
        btnBracket.classList.remove('text-slate-500', 'dark:text-slate-400');
        
        btnStandings.classList.remove('bg-white', 'dark:bg-slate-700', 'text-nba-blue', 'shadow-sm');
        btnStandings.classList.add('text-slate-500', 'dark:text-slate-400');
    }
};
