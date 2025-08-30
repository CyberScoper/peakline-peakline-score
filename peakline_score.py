# /opt/strava-web/utils/peakline_score.py

import math
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class PeakLineScoreCalculator:
    """
    Калькулятор PeakLine Score (PLS) - аналог GFR от Garmin.
    
    Алгоритм:
    1. Анализирует GPX файл (дистанция, набор высоты, градиент)
    2. Рассчитывает "идеальное" время для супер-атлета
    3. Сравнивает реальное время с идеальным
    4. Выдает баллы от 0 до 1000
    """
    
    def __init__(self):
        # Базовые параметры "супер-атлета"
        self.SUPER_ATHLETE_PARAMS = {
            'ftp': 400,  # Watts - топовый FTP
            'max_speed_flat': 55,  # км/ч - максимальная скорость на равнине
            'climbing_power': 6.5,  # Watts/kg - мощность на подъеме
            'weight': 70,  # кг - вес атлета
            'aero_efficiency': 0.95,  # коэффициент аэродинамики
            'rolling_resistance': 0.003,  # коэффициент сопротивления качению
        }
        
        # Коэффициенты для разных типов местности
        self.TERRAIN_COEFFICIENTS = {
            'flat': 1.0,        # равнина
            'rolling': 1.1,     # холмистая местность
            'hilly': 1.25,      # горная местность
            'mountain': 1.5,    # высокогорье
        }
    
    def calculate_score(self, activity_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Основная функция расчета PeakLine Score.
        
        Args:
            activity_data: Данные активности с полями:
                - distance: дистанция в метрах
                - moving_time: время движения в секундах
                - total_elevation_gain: набор высоты в метрах
                - average_speed: средняя скорость в м/с
                - type: тип активности ('Ride', 'Run', etc.)
                - streams: данные потоков (опционально)
        
        Returns:
            Dict с результатами расчета или None если данных недостаточно
        """
        try:
            # Проверяем наличие необходимых данных
            if not self._validate_activity_data(activity_data):
                logger.warning("Insufficient data for PeakLine Score calculation")
                return None
            
            # Извлекаем базовые параметры
            distance_km = activity_data['distance'] / 1000
            moving_time_hours = activity_data['moving_time'] / 3600
            elevation_gain = activity_data.get('total_elevation_gain', 0)
            activity_type = activity_data.get('type', 'Ride')
            
            # Рассчитываем идеальное время
            ideal_time = self._calculate_ideal_time(
                distance_km, 
                elevation_gain, 
                activity_type
            )
            
            if ideal_time is None:
                logger.warning("Could not calculate ideal time")
                return None
            
            # Рассчитываем PLS баллы
            actual_time_hours = moving_time_hours
            time_ratio = ideal_time / actual_time_hours if actual_time_hours > 0 else 0
            
            # Баллы от 0 до 1000
            pls_points = min(1000, max(0, int(time_ratio * 1000)))
            
            # Дополнительная аналитика
            terrain_type = self._classify_terrain(distance_km, elevation_gain)
            difficulty_factor = self._calculate_difficulty_factor(distance_km, elevation_gain)
            
            result = {
                'pls_points': pls_points,
                'ideal_time_hours': round(ideal_time, 2),
                'actual_time_hours': round(actual_time_hours, 2),
                'time_ratio': round(time_ratio, 3),
                'terrain_type': terrain_type,
                'difficulty_factor': round(difficulty_factor, 2),
                'performance_level': self._get_performance_level(pls_points),
                'analysis': self._generate_analysis(pls_points, terrain_type, difficulty_factor)
            }
            
            logger.info(f"PeakLine Score calculated: {pls_points} points")
            return result
            
        except Exception as e:
            logger.exception(f"Error calculating PeakLine Score: {e}")
            return None
    
    def _validate_activity_data(self, data: Dict[str, Any]) -> bool:
        """Проверяет наличие необходимых данных для расчета"""
        required_fields = ['distance', 'moving_time']
        return all(field in data and data[field] is not None for field in required_fields)
    
    def _calculate_ideal_time(self, distance_km: float, elevation_gain: float, activity_type: str) -> Optional[float]:
        """
        Рассчитывает идеальное время для супер-атлета.
        
        Учитывает:
        - Базовую скорость на равнине
        - Влияние набора высоты
        - Тип активности
        - Аэродинамику и сопротивление
        """
        if distance_km <= 0:
            return None
        
        # Базовая скорость в зависимости от типа активности
        if activity_type == 'Run':
            base_speed_kmh = 20  # км/ч для бега
            climbing_penalty = 0.5  # минут на 100м набора высоты
        else:  # Велосипед по умолчанию
            base_speed_kmh = self.SUPER_ATHLETE_PARAMS['max_speed_flat']
            climbing_penalty = 0.3  # минут на 100м набора высоты
        
        # Время на равнине
        flat_time_hours = distance_km / base_speed_kmh
        
        # Штраф за набор высоты
        elevation_penalty_minutes = (elevation_gain / 100) * climbing_penalty
        elevation_penalty_hours = elevation_penalty_minutes / 60
        
        # Коэффициент сложности маршрута
        terrain_coefficient = self._get_terrain_coefficient(distance_km, elevation_gain)
        
        # Итоговое идеальное время
        ideal_time = (flat_time_hours + elevation_penalty_hours) * terrain_coefficient
        
        return ideal_time
    
    def _classify_terrain(self, distance_km: float, elevation_gain: float) -> str:
        """Классифицирует тип местности"""
        if distance_km == 0:
            return 'flat'
        
        elevation_ratio = elevation_gain / (distance_km * 1000)  # м/м
        
        if elevation_ratio < 0.01:
            return 'flat'
        elif elevation_ratio < 0.03:
            return 'rolling'
        elif elevation_ratio < 0.06:
            return 'hilly'
        else:
            return 'mountain'
    
    def _get_terrain_coefficient(self, distance_km: float, elevation_gain: float) -> float:
        """Возвращает коэффициент сложности местности"""
        terrain_type = self._classify_terrain(distance_km, elevation_gain)
        return self.TERRAIN_COEFFICIENTS.get(terrain_type, 1.0)
    
    def _calculate_difficulty_factor(self, distance_km: float, elevation_gain: float) -> float:
        """Рассчитывает общий коэффициент сложности маршрута"""
        # Базовый коэффициент от дистанции
        distance_factor = 1.0 + (distance_km / 100) * 0.1
        
        # Коэффициент от набора высоты
        elevation_factor = 1.0 + (elevation_gain / 1000) * 0.2
        
        # Комбинированный коэффициент
        combined_factor = distance_factor * elevation_factor
        
        return min(3.0, combined_factor)  # Максимум 3.0
    
    def _get_performance_level(self, pls_points: int) -> str:
        """Определяет уровень производительности по баллам"""
        if pls_points >= 900:
            return 'Elite'
        elif pls_points >= 800:
            return 'Excellent'
        elif pls_points >= 700:
            return 'Very Good'
        elif pls_points >= 600:
            return 'Good'
        elif pls_points >= 500:
            return 'Average'
        elif pls_points >= 400:
            return 'Fair'
        else:
            return 'Needs Improvement'
    
    def _generate_analysis(self, pls_points: int, terrain_type: str, difficulty_factor: float) -> str:
        """Генерирует текстовый анализ результата"""
        performance_level = self._get_performance_level(pls_points)
        
        terrain_descriptions = {
            'flat': 'равнинной местности',
            'rolling': 'холмистой местности',
            'hilly': 'горной местности',
            'mountain': 'высокогорья'
        }
        
        terrain_desc = terrain_descriptions.get(terrain_type, 'смешанной местности')
        
        analysis = f"Результат {pls_points} баллов соответствует уровню '{performance_level}' "
        analysis += f"для маршрута по {terrain_desc}. "
        
        if difficulty_factor > 2.0:
            analysis += "Маршрут имеет высокую сложность. "
        elif difficulty_factor > 1.5:
            analysis += "Маршрут средней сложности. "
        else:
            analysis += "Относительно простой маршрут. "
        
        if pls_points >= 800:
            analysis += "Отличная производительность!"
        elif pls_points >= 600:
            analysis += "Хорошая производительность."
        else:
            analysis += "Есть потенциал для улучшения."
        
        return analysis

    def calculate_user_pls_score(self, user_activities: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Рассчитывает общий PLS Score пользователя на основе последних активностей.
        Аналог GFR Score - среднее из 6 лучших результатов.
        """
        if not user_activities:
            return None
        
        # Рассчитываем PLS для каждой активности
        pls_scores = []
        for activity in user_activities:
            score_data = self.calculate_score(activity)
            if score_data:
                pls_scores.append({
                    'activity_id': activity.get('id'),
                    'activity_name': activity.get('name', 'Unknown'),
                    'date': activity.get('start_date'),
                    'pls_points': score_data['pls_points'],
                    'terrain_type': score_data['terrain_type'],
                    'performance_level': score_data['performance_level']
                })
        
        if not pls_scores:
            return None
        
        # Сортируем по баллам (лучшие сначала)
        pls_scores.sort(key=lambda x: x['pls_points'], reverse=True)
        
        # Берем топ-6 результатов
        top_scores = pls_scores[:6]
        
        # Рассчитываем средний балл
        average_pls = sum(score['pls_points'] for score in top_scores) / len(top_scores)
        
        result = {
            'overall_pls_score': round(average_pls, 1),
            'performance_level': self._get_performance_level(int(average_pls)),
            'top_scores': top_scores,
            'total_activities_analyzed': len(pls_scores),
            'improvement_potential': self._calculate_improvement_potential(pls_scores)
        }
        
        return result
    
    def _calculate_improvement_potential(self, pls_scores: List[Dict[str, Any]]) -> str:
        """Анализирует потенциал для улучшения"""
        if len(pls_scores) < 3:
            return "Недостаточно данных для анализа тренда"
        
        # Смотрим на последние 3 результата
        recent_scores = [score['pls_points'] for score in pls_scores[-3:]]
        
        # Проверяем тренд
        if recent_scores[-1] > recent_scores[0]:
            return "Положительная динамика - продолжайте в том же духе!"
        elif recent_scores[-1] < recent_scores[0]:
            return "Есть потенциал для улучшения - проанализируйте тренировочный процесс"
        else:
            return "Стабильные результаты - попробуйте новые вызовы"


# Вспомогательные функции для интеграции с существующим кодом

def calculate_peakline_score_for_activity(activity_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Удобная функция для расчета PLS для одной активности.
    Интегрируется с существующим analyze_activity().
    """
    calculator = PeakLineScoreCalculator()
    return calculator.calculate_score(activity_data)

def add_pls_to_activity_analysis(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Добавляет PLS к существующему анализу активности.
    """
    if not analysis_data or 'details' not in analysis_data:
        return analysis_data
    
    # Извлекаем данные для PLS
    details = analysis_data['details']
    activity_data = {
        'distance': details.get('distance', 0),
        'moving_time': details.get('moving_time', 0),
        'total_elevation_gain': details.get('total_elevation_gain', 0),
        'average_speed': details.get('average_speed', 0),
        'type': details.get('type', 'Ride'),
        'id': details.get('id'),
        'name': details.get('name'),
        'start_date': details.get('start_date')
    }
    
    # Рассчитываем PLS
    pls_data = calculate_peakline_score_for_activity(activity_data)
    
    if pls_data:
        analysis_data['peakline_score'] = pls_data
        logger.info(f"Added PLS {pls_data['pls_points']} to activity analysis")
    
    return analysis_data 
