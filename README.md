# TP4 - Análisis de grafos web

Este proyecto trabaja con el archivo `web-Google.txt`, que modela un grafo dirigido de páginas web y los enlaces existentes entre ellas. Sobre este grafo se desarrollan herramientas para responder distintas preguntas de análisis de redes.

## Objetivos

1. Obtener las componentes conexas del grafo.
2. Calcular caminos mínimos entre páginas.
3. Detectar triángulos.
4. Estimar el PageRank de cada vértice.
5. Medir el diámetro y la circunferencia del grafo.

## Puntos extra

- Contar ciclos de `k` lados.
- Calcular el *clustering coefficient* global y por vértice.
- Calcular la *betweenness centrality* de los vértices.

## Cómo ejecutar

La lectura del archivo y la construcción del grafo se realizan en `tp4.py`.

### Por consola

```bash
python tp4.py
```

### Desde Python

```python
import tp4
# usar las funciones/clases según sea necesario
```

## Dependencias

- Python 3
