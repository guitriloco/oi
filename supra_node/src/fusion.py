#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classe avançada para fusão de inteligências Claude-Gemini
Local: FUSAO_EXTREMA/arsenal/intelligence_fusion.py
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('FUSAO_EXTREMA/logs/fusion_log.txt'),
        logging.StreamHandler()
    ]
)

@dataclass
class ResponseWeights:
    """Pesos para diferentes tipos de respostas"""
    analytical: float = 0.5
    creative: float = 0.5
    technical: float = 0.5
    logical: float = 0.5

class IntelligenceFusion:
    """
    Sistema avançado para fundir respostas de Claude e Gemini
    com base em pesos adaptativos e análise de complementariedade
    """

    def __init__(self):
        self.weights = ResponseWeights()
        self.fusion_history = []

    def calculate_synergy_score(self, claude_response: str, gemini_response: str) -> float:
        """
        Calcula o score de sinergia entre duas respostas
        """
        # Análise básica de complementariedade
        claude_words = set(claude_response.lower().split())
        gemini_words = set(gemini_response.lower().split())

        # Palavras únicas em cada resposta indicam complementariedade
        unique_claude = claude_words - gemini_words
        unique_gemini = gemini_words - claude_words

        total_unique = len(unique_claude) + len(unique_gemini)
        total_combined = len(claude_words.union(gemini_words))

        synergy_score = total_unique / total_combined if total_combined > 0 else 0
        return min(synergy_score, 1.0)

    def adaptive_weighting(self, task_type: str, claude_response: str, gemini_response: str) -> Dict[str, float]:
        """
        Ajusta dinamicamente os pesos com base no tipo de tarefa
        """
        weights = {
            'analytical': self.weights.analytical,
            'creative': self.weights.creative,
            'technical': self.weights.technical,
            'logical': self.weights.logical
        }

        # Ajusta pesos com base no tipo de tarefa
        if task_type == 'analysis':
            weights['analytical'] = min(weights['analytical'] * 1.2, 1.0)
            weights['logical'] = min(weights['logical'] * 1.1, 1.0)
        elif task_type == 'creative':
            weights['creative'] = min(weights['creative'] * 1.3, 1.0)
        elif task_type == 'technical':
            weights['technical'] = min(weights['technical'] * 1.25, 1.0)
        elif task_type == 'problem_solving':
            weights['analytical'] = min(weights['analytical'] * 1.1, 1.0)
            weights['logical'] = min(weights['logical'] * 1.2, 1.0)

        return weights

    def fuse_responses(self, claude_response: str, gemini_response: str, task_type: str = 'general') -> Dict[str, Any]:
        """
        Funde respostas de Claude e Gemini com base em pesos adaptativos
        """
        logging.info(f"Iniciando fusão de respostas para tarefa do tipo: {task_type}")

        # Calcula score de sinergia
        synergy_score = self.calculate_synergy_score(claude_response, gemini_response)

        # Obtém pesos adaptativos
        weights = self.adaptive_weighting(task_type, claude_response, gemini_response)

        # Combina as respostas de forma inteligente
        combined_parts = []

        # Partes analíticas (prioriza Claude para análise técnica)
        if weights['analytical'] > 0.5:
            combined_parts.append(f"[Análise Técnica] {claude_response[:len(claude_response)//2]}")

        # Partes criativas (prioriza Gemini para insights criativos)
        if weights['creative'] > 0.5:
            combined_parts.append(f"[Insight Criativo] {gemini_response[:len(gemini_response)//2]}")

        # Partes lógicas (combina raciocínio de ambos)
        if weights['logical'] > 0.4:
            combined_parts.append(f"[Raciocínio Lógico] Claude: {claude_response[len(claude_response)//2:][:100]} | Gemini: {gemini_response[len(gemini_response)//2:][:100]}")

        # Partes técnicas (prioriza Claude para detalhes técnicos)
        if weights['technical'] > 0.5:
            combined_parts.append(f"[Detalhes Técnicos] {claude_response[len(claude_response)//2:]}")

        # Cria resposta fundida
        fused_response = "\n".join(combined_parts)

        # Informações adicionais
        fusion_data = {
            'fused_response': fused_response,
            'synergy_score': synergy_score,
            'weights_used': weights,
            'claude_input_length': len(claude_response),
            'gemini_input_length': len(gemini_response),
            'fusion_timestamp': time.time()
        }

        # Armazena no histórico
        self.fusion_history.append(fusion_data)

        logging.info(f"Fusão concluída com score de sinergia: {synergy_score:.2f}")

        return fusion_data

    def get_optimized_prompt(self, original_prompt: str, task_type: str) -> str:
        """
        Retorna uma versão otimizada do prompt para melhor aproveitamento da IA
        """
        optimizations = {
            'analysis': f"Analise profundamente '{original_prompt}' explorando múltiplas perspectivas, contrastando com abordagens alternativas e identificando implicações subjacentes.",
            'creative': f"Proponha soluções inovadoras e não ortodoxas para '{original_prompt}', inspirando-se em campos diversos e conexões inesperadas.",
            'technical': f"Detalhe tecnicamente '{original_prompt}' com foco em implementação, especificações e considerações práticas de engenharia.",
            'problem_solving': f"Resolva sistematicamente '{original_prompt}' com raciocínio passo a passo, hipóteses alternativas e verificação de conclusões."
        }

        return optimizations.get(task_type, original_prompt)

# Função auxiliar para facilitar o uso
def create_fusion_engine():
    """
    Cria e retorna uma instância do motor de fusão
    """
    return IntelligenceFusion()

if __name__ == "__main__":
    print("Módulo de Fusão de Inteligências Claude-Gemini carregado com sucesso!")
    print("Use create_fusion_engine() para iniciar o motor de fusão.")