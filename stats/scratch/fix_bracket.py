import re

with open('stats/templates/stats/standings.html', 'r') as f:
    lines = f.readlines()

new_html = """        <div class="relative overflow-x-auto pb-12">
            <div class="min-w-[1400px] flex gap-6">
                
                <!-- Left Side: Eastern Conference -->
                <div class="flex-1 flex gap-6 items-center">
                    <!-- Round 1 -->
                    <div class="flex flex-col gap-6 flex-1">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center mb-1">Round 1</div>
                        {% for matchup in bracket.East %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm transition-all hover:shadow-md">
                            <div class="p-3 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-2">
                                <div class="flex items-center gap-2">
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28">{{ matchup.high.TeamName }}</span>
                                </div>
                                <span class="text-sm font-black {% if matchup.wins > matchup.losses %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.wins }}</span>
                            </div>
                            <div class="p-3 flex items-center justify-between gap-2">
                                <div class="flex items-center gap-2">
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28">{{ matchup.low.TeamName }}</span>
                                </div>
                                <span class="text-sm font-black {% if matchup.losses > matchup.wins %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.losses }}</span>
                            </div>
                        </div>
                        {% empty %}
                        <div class="text-slate-400 text-[10px] text-center border-2 border-dashed border-slate-100 dark:border-slate-800 rounded-xl py-8">Séries Concluídas</div>
                        {% endfor %}
                    </div>

                    <!-- Conference Semis -->
                    <div class="flex flex-col gap-16 flex-1">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center mb-1">Semis</div>
                        {% for matchup in bracket.SemisEast %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm transition-all hover:shadow-md">
                            <div class="p-3 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-2">
                                <div class="flex items-center gap-2">
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28">{{ matchup.high.TeamName }}</span>
                                </div>
                                <span class="text-sm font-black {% if matchup.wins > matchup.losses %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.wins }}</span>
                            </div>
                            <div class="p-3 flex items-center justify-between gap-2">
                                <div class="flex items-center gap-2">
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28">{{ matchup.low.TeamName }}</span>
                                </div>
                                <span class="text-sm font-black {% if matchup.losses > matchup.wins %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.losses }}</span>
                            </div>
                        </div>
                        {% empty %}
                        <div class="bracket-matchup-empty border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl h-24 flex items-center justify-center text-slate-400 text-[10px] font-bold px-4 text-center">Aguardando Round 1</div>
                        <div class="bracket-matchup-empty border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl h-24 flex items-center justify-center text-slate-400 text-[10px] font-bold px-4 text-center">Aguardando Round 1</div>
                        {% endfor %}
                    </div>

                    <!-- Conference Finals -->
                    <div class="flex flex-col gap-6 flex-1">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center mb-1">Final Leste</div>
                        {% for matchup in bracket.FinalsEast %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm transition-all hover:shadow-md">
                            <div class="p-3 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-2">
                                <div class="flex items-center gap-2">
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28">{{ matchup.high.TeamName }}</span>
                                </div>
                                <span class="text-sm font-black">{{ matchup.wins }}</span>
                            </div>
                            <div class="p-3 flex items-center justify-between gap-2">
                                <div class="flex items-center gap-2">
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28">{{ matchup.low.TeamName }}</span>
                                </div>
                                <span class="text-sm font-black">{{ matchup.losses }}</span>
                            </div>
                        </div>
                        {% empty %}
                        <div class="bracket-matchup-empty border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl h-24 flex items-center justify-center text-slate-400 text-[10px] font-bold px-4 text-center font-black uppercase">Campeão Leste</div>
                        {% endfor %}
                    </div>
                </div>

                <!-- Center: NBA Finals -->
                <div class="w-64 flex flex-col items-center justify-center px-4">
                    <div class="text-[11px] font-black text-nba-blue uppercase tracking-[0.3em] mb-4 text-center">NBA Finals</div>
                    <div class="relative group w-full">
                        <div class="absolute -inset-1 bg-gradient-to-r from-nba-blue to-nba-red rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
                        <div class="relative bg-white dark:bg-slate-900 border-2 border-nba-blue/20 rounded-2xl p-6 shadow-2xl flex flex-col items-center gap-4 w-full">
                            {% if bracket.Finals %}
                                <div class="flex flex-col items-center gap-4 w-full">
                                    <div class="flex items-center gap-2 w-full justify-between">
                                        <div class="w-10 h-10 flex items-center justify-center flex-shrink-0">
                                            <img src="https://cdn.nba.com/logos/nba/{{ bracket.Finals.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                        </div>
                                        <span class="text-xl font-black text-slate-800 dark:text-white">{{ bracket.Finals.wins }}</span>
                                    </div>
                                    <div class="text-[10px] font-black text-slate-400 bg-slate-100 dark:bg-slate-800 px-3 py-1 rounded-full uppercase tracking-widest">VS</div>
                                    <div class="flex items-center gap-2 w-full justify-between">
                                        <div class="w-10 h-10 flex items-center justify-center flex-shrink-0">
                                            <img src="https://cdn.nba.com/logos/nba/{{ bracket.Finals.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain">
                                        </div>
                                        <span class="text-xl font-black text-slate-800 dark:text-white">{{ bracket.Finals.losses }}</span>
                                    </div>
                                </div>
                            {% else %}
                                <div class="w-16 h-16 rounded-full bg-gradient-to-br from-yellow-400 to-yellow-600 flex items-center justify-center shadow-lg border-4 border-yellow-200 dark:border-yellow-900 mb-2">
                                    <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                                    </svg>
                                </div>
                                <div class="text-center">
                                    <div class="text-xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-500 to-yellow-700 uppercase tracking-tighter">NBA Finals</div>
                                    <div class="text-[9px] font-bold text-slate-400 tracking-[0.2em] mt-1 uppercase">A Glória Suprema</div>
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>

                <!-- Right Side: Western Conference -->
                <div class="flex-1 flex gap-6 items-center">
                    <!-- Conference Finals -->
                    <div class="flex flex-col gap-6 flex-1">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center mb-1">Final Oeste</div>
                        {% for matchup in bracket.FinalsWest %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm transition-all hover:shadow-md">
                            <div class="p-3 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-2">
                                <span class="text-sm font-black">{{ matchup.wins }}</span>
                                <div class="flex items-center gap-2 justify-end">
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28 text-right">{{ matchup.high.TeamName }}</span>
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                </div>
                            </div>
                            <div class="p-3 flex items-center justify-between gap-2">
                                <span class="text-sm font-black">{{ matchup.losses }}</span>
                                <div class="flex items-center gap-2 justify-end">
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28 text-right">{{ matchup.low.TeamName }}</span>
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                </div>
                            </div>
                        </div>
                        {% empty %}
                        <div class="bracket-matchup-empty border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl h-24 flex items-center justify-center text-slate-400 text-[10px] font-bold px-4 text-center font-black uppercase">Campeão Oeste</div>
                        {% endfor %}
                    </div>

                    <!-- Conference Semis -->
                    <div class="flex flex-col gap-16 flex-1">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center mb-1">Semis</div>
                        {% for matchup in bracket.SemisWest %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm transition-all hover:shadow-md">
                            <div class="p-3 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-2">
                                <span class="text-sm font-black {% if matchup.wins > matchup.losses %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.wins }}</span>
                                <div class="flex items-center gap-2 justify-end">
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28 text-right">{{ matchup.high.TeamName }}</span>
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                </div>
                            </div>
                            <div class="p-3 flex items-center justify-between gap-2">
                                <span class="text-sm font-black {% if matchup.losses > matchup.wins %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.losses }}</span>
                                <div class="flex items-center gap-2 justify-end">
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28 text-right">{{ matchup.low.TeamName }}</span>
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                </div>
                            </div>
                        </div>
                        {% empty %}
                        <div class="bracket-matchup-empty border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl h-24 flex items-center justify-center text-slate-400 text-[10px] font-bold px-4 text-center">Aguardando Round 1</div>
                        <div class="bracket-matchup-empty border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl h-24 flex items-center justify-center text-slate-400 text-[10px] font-bold px-4 text-center">Aguardando Round 1</div>
                        {% endfor %}
                    </div>

                    <!-- Round 1 -->
                    <div class="flex flex-col gap-6 flex-1 text-right">
                        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-widest text-center mb-1">Round 1</div>
                        {% for matchup in bracket.West %}
                        <div class="bracket-matchup bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-xl shadow-sm transition-all hover:shadow-md">
                            <div class="p-3 flex items-center justify-between border-b border-slate-50 dark:border-slate-700/50 gap-2">
                                <span class="text-sm font-black {% if matchup.wins > matchup.losses %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.wins }}</span>
                                <div class="flex items-center gap-2 justify-end">
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28 text-right">{{ matchup.high.TeamName }}</span>
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.high.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                </div>
                            </div>
                            <div class="p-3 flex items-center justify-between gap-2">
                                <span class="text-sm font-black {% if matchup.losses > matchup.wins %}text-emerald-500{% else %}text-slate-400{% endif %}">{{ matchup.losses }}</span>
                                <div class="flex items-center gap-2 justify-end">
                                    <span class="font-bold text-slate-700 dark:text-slate-200 text-xs truncate w-24 sm:w-28 text-right">{{ matchup.low.TeamName }}</span>
                                    <div class="w-6 h-6 flex items-center justify-center flex-shrink-0">
                                        <img src="https://cdn.nba.com/logos/nba/{{ matchup.low.TeamID }}/global/L/logo.svg" class="max-w-full max-h-full object-contain" alt="">
                                    </div>
                                </div>
                            </div>
                        </div>
                        {% empty %}
                        <div class="text-slate-400 text-[10px] text-center border-2 border-dashed border-slate-100 dark:border-slate-800 rounded-xl py-8">Séries Concluídas</div>
                        {% endfor %}
                    </div>
                </div>

            </div>\n"""

lines[204:402] = [new_html]

with open('stats/templates/stats/standings.html', 'w') as f:
    f.writelines(lines)

