from Calc import *

"""
    Calc.CalcToNotation(data: list or tuple , translation: int, printer: boolean) ->
        Format "data" list(tuple(str, int)) or tuple(str, int); int in 2 to 36
        Format "translation" int in 2 to 36
        The "printer" setting outputs the result to the console

    Func "comparison"
        Outputs maximum and minimum in the console

    Example: 'CalcToNotation([('2198129', 10), ('23y42', 35)], 16).comparison()' -> 
        output: '2198129 (10) = 218A71 (16)
                 23y42 (35) = 306553 (16)
                 Max: 306553 || Min: 218A71'
"""

"""
    Calc.CalcToPathUrl(data: str, protocol: str, server: str, file; str) ->
        Format "data" from task body to str separated by space
        Format "protocol" protocol from tasks
        Format "server" server from tasks with extension
        Format "file" file from tasks wit extension

    Example: 'CalcToPathUrl('.txt :// http circ / .org slon', 'http', 'circ.org', 'slon.txt')' -> 
        output: 'Output: "http://circ.org/slon.txt" || Answer "3246571" or "ВБГЕДЖА"'
"""
