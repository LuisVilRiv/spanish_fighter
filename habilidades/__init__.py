"""
Módulo de habilidades para Batalla Cómica Española.
Exporta todas las habilidades organizadas por personaje.
"""

# Habilidades del Segarro
from .habilidades_segarro import (
    DameCartera,
    PedirSigarrito,
    SuperMeca,
    CriticaConstructiva,
    ToPelma,
    PedirFavor
)

# Habilidades de la Católica
from .habilidades_catolico import (
    RezarRosario,
    AguaBendita,
    SermonDominical,
    MiradaJuzgadora,
    ViernesSanto,
    Excomulgar
)

# Habilidades del Sacerdote
from .habilidades_sacerdote import (
    Exorcismo,
    BendicionDivina,
    AguaBenditaAvanzada,
    SermonEterno,
    MilagroDivino,
    CastigoDivino
)

# Habilidades de la Abuela
from .habilidades_abuela import (
    CucharonDeMadera,
    ComeHijo,
    ChismeVenenoso,
    RemedioCasero,
    MiradaQueMata,
    BufandaDeLana
)

# Habilidades del Barrendero
from .habilidades_barrendero import (
    BarridoExistencial,
    FregonaDeLaVerdad,
    CuboDeLaSabiduria,
    MeditacionCallejera,
    FilosofiaDeBar,
    LimpiezaProfunda
)

# Habilidades de la Choni
from .habilidades_choni import (
    TacónEnElPie,
    MiradaDeHielo,
    SelfieConFiltro,
    Uñazo,
    Chismorreo,
    FiestaDelPueblo
)

# Habilidades del Flaquito
from .habilidades_flaquito import (
    ArenaEnLosOjos,
    SurfearOla,
    BronceadoExpress,
    Esquivel,
    PalizaDeToalla,
    RefrescoAzucarado
)

# Habilidades del Político
from .habilidades_politico import (
    DiscursoVacio,
    PromesaFalsa,
    FotoConBebe,
    DesviarAtencion,
    SubirImpuestos,
    CampanaElectoral
)

# Habilidades del PutoAmo
from .habilidades_putamo import (
    FlexionExplosiva,
    BatidoDeProteinas,
    SelfieEnElEspejo,
    Levantamiento,
    GritoDeGuerra,
    RutinaExtrema
)

# Habilidades del Torero
from .habilidades_torero import (
    PaseDeTorero,
    Estocada,
    OlesDelPublico,
    Capote,
    Finta,
    Faena
)

# Habilidades del Turista
from .habilidades_turista import (
    PedirDirecciones,
    FotoTuristica,
    ComprarSouvenir,
    Perderse,
    HablarInglesAlto,
    BuscarWifi
)

# Exportar todo
__all__ = [
    # Segarro
    'DameCartera',
    'PedirSigarrito',
    'SuperMeca',
    'CriticaConstructiva',
    'ToPelma',
    'PedirFavor',
    
    # Católica
    'RezarRosario',
    'AguaBendita',
    'SermonDominical',
    'MiradaJuzgadora',
    'ViernesSanto',
    'Excomulgar',
    
    # Sacerdote
    'Exorcismo',
    'BendicionDivina',
    'AguaBenditaAvanzada',
    'SermonEterno',
    'MilagroDivino',
    'CastigoDivino',
    
    # Abuela
    'CucharonDeMadera',
    'ComeHijo',
    'ChismeVenenoso',
    'RemedioCasero',
    'MiradaQueMata',
    'BufandaDeLana',
    
    # Barrendero
    'BarridoExistencial',
    'FregonaDeLaVerdad',
    'CuboDeLaSabiduria',
    'MeditacionCallejera',
    'FilosofiaDeBar',
    'LimpiezaProfunda',
    
    # Choni
    'TacónEnElPie',
    'MiradaDeHielo',
    'SelfieConFiltro',
    'Uñazo',
    'Chismorreo',
    'FiestaDelPueblo',
    
    # Flaquito
    'ArenaEnLosOjos',
    'SurfearOla',
    'BronceadoExpress',
    'Esquivel',
    'PalizaDeToalla',
    'RefrescoAzucarado',
    
    # Político
    'DiscursoVacio',
    'PromesaFalsa',
    'FotoConBebe',
    'DesviarAtencion',
    'SubirImpuestos',
    'CampanaElectoral',
    
    # PutoAmo
    'FlexionExplosiva',
    'BatidoDeProteinas',
    'SelfieEnElEspejo',
    'Levantamiento',
    'GritoDeGuerra',
    'RutinaExtrema',
    
    # Torero
    'PaseDeTorero',
    'Estocada',
    'OlesDelPublico',
    'Capote',
    'Finta',
    'Faena',
    
    # Turista
    'PedirDirecciones',
    'FotoTuristica',
    'ComprarSouvenir',
    'Perderse',
    'HablarInglesAlto',
    'BuscarWifi'
]