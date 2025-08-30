# /utils/activity_analyzer.py
from .peakline_score import add_pls_to_activity_analysis

async def analyze_activity(activity_id: str, strava_user_id: int):
    # ... здесь происходит весь основной анализ ...
    # ... получение данных из Strava, расчет зон и т.д. ...
    
    # В конце, когда все данные собраны в analysis_results:
    set_cached_analysis(int(activity_id), strava_user_id, analysis_results)
    
    # Добавляем PeakLine Score к анализу
    analysis_results = add_pls_to_activity_analysis(analysis_results)
    
    logger.info(f"Analysis for activity {activity_id} completed successfully.")
    return analysis_results
