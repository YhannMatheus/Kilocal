from src.types.enums.exercise import MuscleGroupEnum

DEFAULT_EXERCISES = [
    # --- PEITORAL (CHEST) ---
    {
        "name": "Supino Reto (Barra)",
        "target_muscle": MuscleGroupEnum.CHEST,
        "instructions": "Deite-se no banco, segure a barra na largura dos ombros, desça até o peito e empurre para cima."
    },
    {
        "name": "Supino Reto (Halteres)",
        "target_muscle": MuscleGroupEnum.CHEST,
        "instructions": "Deite-se no banco, segure os halteres, desça controlando e empurre unindo-os no topo."
    },
    {
        "name": "Supino Inclinado (Barra)",
        "target_muscle": MuscleGroupEnum.CHEST,
        "instructions": "Banco inclinado (30-45 graus). Foco na porção superior do peitoral."
    },
    {
        "name": "Supino Inclinado (Halteres)",
        "target_muscle": MuscleGroupEnum.CHEST,
        "instructions": "Banco inclinado. Foco na porção superior com maior amplitude que a barra."
    },
    {
        "name": "Crucifixo (Halteres)",
        "target_muscle": MuscleGroupEnum.CHEST,
        "instructions": "Abertura lateral dos braços deitado no banco, mantendo leve flexão dos cotovelos."
    },
    {
        "name": "Crossover (Polia Alta)",
        "target_muscle": MuscleGroupEnum.CHEST,
        "instructions": "Puxe os cabos de cima para baixo e para o centro, focando na contração inferior."
    },
    {
        "name": "Peck Deck / Voador",
        "target_muscle": MuscleGroupEnum.CHEST,
        "instructions": "Máquina para isolamento do peitoral. Mantenha os cotovelos alinhados."
    },
    {
        "name": "Flexão de Braços (Push-up)",
        "target_muscle": MuscleGroupEnum.CHEST,
        "instructions": "Exercício com peso do corpo. Mantenha o corpo reto e desça até o peito quase tocar o chão."
    },

    # --- COSTAS (BACK) ---
    {
        "name": "Puxada Frontal (Polia)",
        "target_muscle": MuscleGroupEnum.BACK,
        "instructions": "Puxe a barra em direção ao peito, focando em esmagar as escápulas."
    },
    {
        "name": "Remada Curvada (Barra)",
        "target_muscle": MuscleGroupEnum.BACK,
        "instructions": "Incline o tronco à frente, mantenha a coluna reta e puxe a barra na direção do umbigo."
    },
    {
        "name": "Remada Unilateral (Serrote)",
        "target_muscle": MuscleGroupEnum.BACK,
        "instructions": "Apoie-se no banco e puxe o halter lateralmente, trazendo o cotovelo para trás."
    },
    {
        "name": "Levantamento Terra",
        "target_muscle": MuscleGroupEnum.BACK,
        "instructions": "Levante a barra do chão estendendo o quadril e joelhos. Mantendo a postura correta."
    },
    {
        "name": "Barra Fixa (Pull-up)",
        "target_muscle": MuscleGroupEnum.BACK,
        "instructions": "Pendure-se na barra e puxe o corpo para cima até o queixo passar da barra."
    },
    {
        "name": "Remada Baixa (Triângulo)",
        "target_muscle": MuscleGroupEnum.BACK,
        "instructions": "Sentado na máquina, puxe o triângulo em direção ao abdômen."
    },
    {
        "name": "Pulldown (Frente)",
        "target_muscle": MuscleGroupEnum.BACK,
        "instructions": "Braços estendidos, puxe a barra da linha da cabeça até a coxa, ativando a dorsal."
    },

    # --- PERNAS (LEGS) ---
    {
        "name": "Agachamento Livre (Barra)",
        "target_muscle": MuscleGroupEnum.LEGS,
        "instructions": "Barra nas costas, desça flexionando joelhos e quadril, mantendo coluna alinhada."
    },
    {
        "name": "Leg Press 45",
        "target_muscle": MuscleGroupEnum.LEGS,
        "instructions": "Empurre a plataforma com as pernas, sem estender totalmente os joelhos (bloquear) no final."
    },
    {
        "name": "Cadeira Extensora",
        "target_muscle": MuscleGroupEnum.LEGS,
        "instructions": "Estenda os joelhos para trabalhar o quadríceps. Segure no topo por 1s."
    },
    {
        "name": "Cadeira Flexora",
        "target_muscle": MuscleGroupEnum.LEGS,
        "instructions": "Sentado, flexione os joelhos trazendo o suporte para baixo. Foco em posterior."
    },
    {
        "name": "Mesa Flexora",
        "target_muscle": MuscleGroupEnum.LEGS,
        "instructions": "Deitado, flexione os joelhos trazendo o suporte em direção ao glúteo."
    },
    {
        "name": "Stiff (Barra/Halteres)",
        "target_muscle": MuscleGroupEnum.LEGS,
        "instructions": "Pernas quase esticadas, desça o tronco mantendo a coluna reta, sentindo alongar o posterior."
    },
    {
        "name": "Afundo / Passada",
        "target_muscle": MuscleGroupEnum.LEGS,
        "instructions": "Dê um passo à frente e desça o joelho de trás em direção ao chão."
    },
    {
        "name": "Elevação Pélvica",
        "target_muscle": MuscleGroupEnum.LEGS,
        "instructions": "Apoie as costas no banco e levante o quadril contraindo os glúteos."
    },
    {
        "name": "Panturrilha em Pé",
        "target_muscle": MuscleGroupEnum.LEGS,
        "instructions": "Eleve os calcanhares o máximo possível e desça controlando."
    },
    {
        "name": "Panturrilha Sentado",
        "target_muscle": MuscleGroupEnum.LEGS,
        "instructions": "Máquina específica para panturrilha sentado. Foco no músculo sóleo."
    },

    # --- OMBROS (SHOULDERS) ---
    {
        "name": "Desenvolvimento (Barra/Halteres)",
        "target_muscle": MuscleGroupEnum.SHOULDERS,
        "instructions": "Empurre o peso acima da cabeça, estendendo os braços."
    },
    {
        "name": "Elevação Lateral",
        "target_muscle": MuscleGroupEnum.SHOULDERS,
        "instructions": "Abra os braços lateralmente até a altura dos ombros."
    },
    {
        "name": "Elevação Frontal",
        "target_muscle": MuscleGroupEnum.SHOULDERS,
        "instructions": "Levante o peso à frente do corpo até a altura dos ombros."
    },
    {
        "name": "Crucifixo Inverso / Posterior de Ombros",
        "target_muscle": MuscleGroupEnum.SHOULDERS,
        "instructions": "Incline o tronco ou use a máquina (voador invertido) para abrir os braços para trás."
    },
    {
        "name": "Encolhimento (Trapézio)",
        "target_muscle": MuscleGroupEnum.SHOULDERS,
        "instructions": "Eleve os ombros em direção às orelhas segurando pesos."
    },

    # --- BRAÇOS (ARMS - Biceps/Triceps) ---
    {
        "name": "Rosca Direta (Barra)",
        "target_muscle": MuscleGroupEnum.ARMS,
        "instructions": "Flexione os cotovelos trazendo a barra até o peito. Mantenha cotovelos fixos."
    },
    {
        "name": "Rosca Alternada (Halteres)",
        "target_muscle": MuscleGroupEnum.ARMS,
        "instructions": "Flexione um braço de cada vez, girando o punho na subida."
    },
    {
        "name": "Rosca Martelo",
        "target_muscle": MuscleGroupEnum.ARMS,
        "instructions": "Pegada neutra (palmas viradas uma para a outra), foca no braquial."
    },
    {
        "name": "Rosca Scott",
        "target_muscle": MuscleGroupEnum.ARMS,
        "instructions": "Apoiado no banco Scott, isolando o bíceps."
    },
    {
        "name": "Tríceps Polia (Barra/Corda)",
        "target_muscle": MuscleGroupEnum.ARMS,
        "instructions": "Estenda o cotovelo empurrando o peso para baixo."
    },
    {
        "name": "Tríceps Testa",
        "target_muscle": MuscleGroupEnum.ARMS,
        "instructions": "Deitado, desça o peso em direção à testa flexionando os cotovelos e estenda novamente."
    },
    {
        "name": "Tríceps Francês",
        "target_muscle": MuscleGroupEnum.ARMS,
        "instructions": "Segure o peso atrás da cabeça e estenda os braços para cima."
    },
    {
        "name": "Mergulho (Barra Paralela/Banco)",
        "target_muscle": MuscleGroupEnum.ARMS,
        "instructions": "Desça o corpo flexionando os cotovelos e empurre para subir."
    },

    # --- ABDOMEN ---
    {
        "name": "Abdominal Supra (Chão)",
        "target_muscle": MuscleGroupEnum.ABDOMEN,
        "instructions": "Flexione o tronco tirando as escápulas do chão."
    },
    {
        "name": "Abdominal Infra (Elevação de Pernas)",
        "target_muscle": MuscleGroupEnum.ABDOMEN,
        "instructions": "Eleve as pernas mantendo o tronco estavel."
    },
    {
        "name": "Prancha Isométrica",
        "target_muscle": MuscleGroupEnum.ABDOMEN,
        "instructions": "Mantenha o corpo reto apoiado nos antebraços e ponta dos pés."
    },
    {
        "name": "Abdominal Rimador",
        "target_muscle": MuscleGroupEnum.ABDOMEN,
        "instructions": "Estenda o corpo todo e abrace os joelhos flexionando o tronco."
    },

    # --- CARDIO ---
    {
        "name": "Esteira (Corrida)",
        "target_muscle": MuscleGroupEnum.CARDIO,
        "instructions": "Corrida contínua ou intervalada."
    },
    {
        "name": "Esteira (Caminhada)",
        "target_muscle": MuscleGroupEnum.CARDIO,
        "instructions": "Caminhada em ritmo moderado."
    },
    {
        "name": "Bicicleta Ergométrica",
        "target_muscle": MuscleGroupEnum.CARDIO,
        "instructions": "Pedalada contínua."
    },
    {
        "name": "Elíptico / Transport",
        "target_muscle": MuscleGroupEnum.CARDIO,
        "instructions": "Movimento simulando corrida sem impacto."
    },
    {
        "name": "Pular Corda",
        "target_muscle": MuscleGroupEnum.CARDIO,
        "instructions": "Saltos contínuos girando a corda."
    },
]
