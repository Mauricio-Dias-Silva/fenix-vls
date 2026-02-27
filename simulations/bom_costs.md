# Fênix VLS - Bill of Materials (BoM) e Estimativa de Custo (Protótipo Alpha)

Este documento detalha os componentes necessários para construir o protótipo físico do Fênix VLS (Duração de voo estimada: 3-5 minutos, Controle via LLM Local).

## 1. Estrutura e Chassi (Airframe)
Para o esqueleto principal, usaremos alumínio aeronáutico e fibra de carbono devido ao custo-benefício em relação ao Titânio puro nesta fase inicial.

| Item | Descrição / Especificação | Qtd | Valor Est. (BRL) | Valor Est. (USD) |
| :--- | :--- | :--- | :--- | :--- |
| **Tubos de Fibra de Carbono (CFRP)** | Diâmetro Externo 25mm, Parede 1.5mm (Estrutura cruzada) | 4 un | R$ 380,00 | $ 75.00 |
| **Chapas de Alumínio 7075-T6** | Corte CNC para os nós de junção e base do motor | 1 m² | R$ 450,00 | $ 90.00 |
| **Parafusos e Fixação em Titânio** | Resistência à torção sem ganho de massa | 1 kit | R$ 200,00 | $ 40.00 |
| **Tinta Condutiva / Absorção Radar** | Mistura base para simular RAM (Radar Absorbent Material) | 1 lt | R$ 150,00 | $ 30.00 |
| **Subtotal Chassi** | | | **R$ 1.180,00** | **$ 235.00** |

## 2. Propulsão Vetorizada (Quantum Inertial Drive - Simulação)
Nesta fase, o QID é traduzido em força eletromecânica bruta vetorizada.

| Item | Descrição / Especificação | Qtd | Valor Est. (BRL) | Valor Est. (USD) |
| :--- | :--- | :--- | :--- | :--- |
| **Motores EDF (Electric Ducted Fan) 90mm** | Empuxo de ~4.5kg cada (Configuração bi-motor contra-rotativa) | 2 un | R$ 1.400,00 | $ 280.00 |
| **ESC (Eletronic Speed Controller) 120A** | Alta corrente para suportar picos aerodinâmicos | 2 un | R$ 650,00 | $ 130.00 |
| **Micro-Servos de Titânio (Atuadores)** | High-Torque / High-Speed para o Thrust Vectoring no bocal | 4 un | R$ 320,00 | $ 64.00 |
| **Bateria LiPo 6S (22.2V) 6000mAh 60C** | Densidade de energia máxima para tempo de hover | 2 un | R$ 900,00 | $ 180.00 |
| **Subtotal Propulsão** | | | **R$ 3.270,00** | **$ 654.00** |

## 3. Cérebro Cognitivo (Sensor Fusion e LLM Node)
A computação embarcada responsável por rodar o `physics_engine.py` e o LLM Local de comunicação.

| Item | Descrição / Especificação | Qtd | Valor Est. (BRL) | Valor Est. (USD) |
| :--- | :--- | :--- | :--- | :--- |
| **Placa Base (Cérebro)** | NVIDIA Jetson Orin Nano (8GB) - Poder de IA na placa | 1 un | R$ 3.500,00 | $ 700.00 |
| **IMU Militar 9-Eixos (BNO085/BNO055)** | Telemetria de Atitude sem Glitch de estabilização | 1 un | R$ 250,00 | $ 50.00 |
| **Lidar Sensor (TFmini-S)** | Altímetro a laser (Ground Effect Mitigation) | 1 un | R$ 300,00 | $ 60.00 |
| **Interface/Transmissor Telemetria** | LoRaWAN ou RF 900MHz para ligar ao VLS Command Center | 1 un | R$ 180,00 | $ 36.00 |
| **Subtotal Aviônica** | | | **R$ 4.230,00** | **$ 846.00** |

---

## INVESTIMENTO TOTAL ESTIMADO:
**BRL: R$ 8.680,00**  
*(Aproximadamente USD: $ 1.735,00)*

## Conclusões de Engenharia
- O Protótipo Alpha com esta configuração de EDF dupla pesará em média 4.5kg (com bateria).
- Os motores entregam juntos ~9kg de empuxo. A janela de "Power-to-weight ratio" (Taxa Peso-Potência) é de 2:1. É o suficiente para o "Hovering" absoluto e subida agressiva.
- O cérebro (Jetson) garante a execução offline das rotinas Django (painel), LLM (voz) e Física sem *delay*.
