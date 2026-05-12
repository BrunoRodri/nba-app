import re

with open('stats/templates/stats/standings.html', 'r') as f:
    lines = f.readlines()

# Extract the content between start and end of bracket
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '<div class="relative overflow-x-auto pb-12">' in line:
        start_idx = i
    if '{% endif %}' in line and i > start_idx and start_idx != -1:
        # Assuming the first {% endif %} after the bracket start is the correct one
        end_idx = i
        break

if start_idx == -1 or end_idx == -1:
    print("Could not find bracket bounds")
    exit(1)

# I'll just rewrite the whole tab-bracket content for safety
# First find the tab-bracket div start
tab_start = -1
for i, line in enumerate(lines):
    if 'id="tab-bracket"' in line:
        tab_start = i
        break

new_tab_content = """    <div id="tab-bracket" class="hidden animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div class="bg-blue-50/50 dark:bg-blue-900/10 border-l-4 border-nba-blue p-4 mb-8 rounded-r-xl">
            <div class="flex items-center gap-3">
                <i class="fas fa-info-circle text-nba-blue"></i>
                <p class="text-sm font-medium">
                    {% if bracket.is_projected %}
                        <strong>Chaveamento Projetado:</strong> Baseado na classificação atual da temporada regular.
                    {% else %}
                        <strong>Bracket Ao Vivo:</strong> Acompanhando as séries de Playoff {{ season }} em tempo real.
                    {% endif %}
                </p>
            </div>
        </div>

        <div class="flex flex-col gap-16 max-w-6xl mx-auto pb-12">
            
            <!-- Conferência Leste -->
            <div class="space-y-6">
                <div class="flex items-center gap-4">
                    <div class="h-px flex-1 bg-slate-200 dark:bg-slate-700"></div>
                    <h3 class="text-xl font-black text-nba-blue uppercase tracking-[0.2em]">Conferência Leste</h3>
                    <div class="h-px flex-1 bg-slate-200 dark:bg-slate-700"></div>
                </div>
                
                <div class="flex gap-8 items-start justify-center overflow-x-auto lg:overflow-visible pb-4">
                    <!-- Round 1 -->
                    <div class="flex flex-col gap-6 w-72 flex-shrink-0">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center">Round 1</div>
                        {% for matchup in bracket.East %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm hover:shadow-md transition-all">
                            <div class="p-4 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.high.TeamName }}</span>
                                </div>
                                <span class="text-base font-black flex-shrink-0 {% if matchup.wins > matchup.losses %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.wins }}</span>
                            </div>
                            <div class="p-4 flex items-center justify-between gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.low.TeamName }}</span>
                                </div>
                                <span class="text-base font-black flex-shrink-0 {% if matchup.losses > matchup.wins %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.losses }}</span>
                            </div>
                        </div>
                        {% endfor %}
                    </div>

                    <!-- Semis -->
                    <div class="flex flex-col gap-6 w-72 flex-shrink-0 pt-16">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center">Semis</div>
                        {% for matchup in bracket.SemisEast %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm hover:shadow-md transition-all">
                            <div class="p-4 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.high.TeamName }}</span>
                                </div>
                                <span class="text-base font-black flex-shrink-0 {% if matchup.wins > matchup.losses %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.wins }}</span>
                            </div>
                            <div class="p-4 flex items-center justify-between gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.low.TeamName }}</span>
                                </div>
                                <span class="text-base font-black flex-shrink-0 {% if matchup.losses > matchup.wins %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.losses }}</span>
                            </div>
                        </div>
                        {% empty %}
                        <div class="h-28 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl"></div>
                        <div class="h-28 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl"></div>
                        {% endfor %}
                    </div>

                    <!-- Finals -->
                    <div class="flex flex-col gap-6 w-72 flex-shrink-0 pt-32">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center">Final Leste</div>
                        {% for matchup in bracket.FinalsEast %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm hover:shadow-md transition-all">
                            <div class="p-4 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.high.TeamName }}</span>
                                </div>
                                <span class="text-base font-black">{{ matchup.wins }}</span>
                            </div>
                            <div class="p-4 flex items-center justify-between gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.low.TeamName }}</span>
                                </div>
                                <span class="text-base font-black">{{ matchup.losses }}</span>
                            </div>
                        </div>
                        {% empty %}
                        <div class="h-28 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl flex items-center justify-center text-[10px] font-black uppercase text-slate-400">Campeão Leste</div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <!-- NBA Finals Centerpiece -->
            <div class="flex flex-col items-center justify-center">
                <div class="text-sm font-black text-slate-400 uppercase tracking-[0.4em] mb-6">NBA Finals</div>
                <div class="relative group">
                    <div class="absolute -inset-1 bg-gradient-to-r from-nba-blue to-nba-red rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
                    <div class="relative bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 rounded-2xl p-8 shadow-2xl flex flex-col items-center gap-6 min-w-[320px]">
                        {% if bracket.Finals %}
                            <div class="flex flex-col items-center gap-6 w-full">
                                <div class="flex items-center gap-4 w-full justify-between">
                                    <div class="w-14 h-14 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ bracket.Finals.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="text-3xl font-black text-slate-800 dark:text-white">{{ bracket.Finals.wins }}</span>
                                </div>
                                <div class="text-[11px] font-black text-slate-400 bg-slate-100 dark:bg-slate-800 px-6 py-2 rounded-full uppercase tracking-[0.2em]">World Champions</div>
                                <div class="flex items-center gap-4 w-full justify-between">
                                    <div class="w-14 h-14 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ bracket.Finals.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="text-3xl font-black text-slate-800 dark:text-white">{{ bracket.Finals.losses }}</span>
                                </div>
                            </div>
                        {% else %}
                            <div class="w-28 h-28 rounded-full bg-gradient-to-br from-yellow-400 to-yellow-600 flex items-center justify-center shadow-lg border-4 border-yellow-100 dark:border-yellow-900 mb-2">
                                <svg class="w-14 h-14 text-white" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                                </svg>
                            </div>
                            <div class="text-center">
                                <div class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-500 to-yellow-700 uppercase tracking-tighter">NBA Finals</div>
                                <div class="text-xs font-bold text-slate-400 tracking-[0.3em] mt-3 uppercase">The Glory Awaits</div>
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>

            <!-- Conferência Oeste -->
            <div class="space-y-6">
                <div class="flex items-center gap-4">
                    <div class="h-px flex-1 bg-slate-200 dark:bg-slate-700"></div>
                    <h3 class="text-xl font-black text-nba-red uppercase tracking-[0.2em]">Conferência Oeste</h3>
                    <div class="h-px flex-1 bg-slate-200 dark:bg-slate-700"></div>
                </div>
                
                <div class="flex gap-8 items-start justify-center overflow-x-auto lg:overflow-visible pb-4">
                    <!-- Round 1 -->
                    <div class="flex flex-col gap-6 w-72 flex-shrink-0">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center">Round 1</div>
                        {% for matchup in bracket.West %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm hover:shadow-md transition-all">
                            <div class="p-4 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.high.TeamName }}</span>
                                </div>
                                <span class="text-base font-black flex-shrink-0 {% if matchup.wins > matchup.losses %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.wins }}</span>
                            </div>
                            <div class="p-4 flex items-center justify-between gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.low.TeamName }}</span>
                                </div>
                                <span class="text-base font-black flex-shrink-0 {% if matchup.losses > matchup.wins %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.losses }}</span>
                            </div>
                        </div>
                        {% endfor %}
                    </div>

                    <!-- Semis -->
                    <div class="flex flex-col gap-6 w-72 flex-shrink-0 pt-16">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center">Semis</div>
                        {% for matchup in bracket.SemisWest %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm hover:shadow-md transition-all">
                            <div class="p-4 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.high.TeamName }}</span>
                                </div>
                                <span class="text-base font-black flex-shrink-0 {% if matchup.wins > matchup.losses %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.wins }}</span>
                            </div>
                            <div class="p-4 flex items-center justify-between gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.low.TeamName }}</span>
                                </div>
                                <span class="text-base font-black flex-shrink-0 {% if matchup.losses > matchup.wins %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.losses }}</span>
                            </div>
                        </div>
                        {% empty %}
                        <div class="h-28 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl"></div>
                        <div class="h-28 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl"></div>
                        {% endfor %}
                    </div>

                    <!-- Finals -->
                    <div class="flex flex-col gap-6 w-72 flex-shrink-0 pt-32">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center">Final Oeste</div>
                        {% for matchup in bracket.FinalsWest %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm hover:shadow-md transition-all">
                            <div class="p-4 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.high.TeamName }}</span>
                                </div>
                                <span class="text-base font-black">{{ matchup.wins }}</span>
                            </div>
                            <div class="p-4 flex items-center justify-between gap-4">
                                <div class="flex items-center gap-3 flex-1 w-0">
                                    <div class="w-8 h-8 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-sm truncate flex-1">{{ matchup.low.TeamName }}</span>
                                </div>
                                <span class="text-base font-black">{{ matchup.losses }}</span>
                            </div>
                        </div>
                        {% empty %}
                        <div class="h-28 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl flex items-center justify-center text-[10px] font-black uppercase text-slate-400">Campeão Oeste</div>
                        {% endfor %}
                    </div>
                </div>
            </div>

        </div>\n"""

# Search for the end of the tab-bracket content
# It ends before the <script> tag usually
script_start = -1
for i, line in enumerate(lines):
    if '<script>' in line and i > tab_start:
        script_start = i
        break

# The tab-bracket ends with </div> repeated a few times.
# We want to replace from tab_start to the line before block extra_js
extra_js_start = -1
for i, line in enumerate(lines):
    if '{% block extra_js %}' in line:
        extra_js_start = i
        break

lines[tab_start:extra_js_start] = [new_tab_content + "\\n"]

with open('stats/templates/stats/standings.html', 'w') as f:
    f.writelines(lines)
