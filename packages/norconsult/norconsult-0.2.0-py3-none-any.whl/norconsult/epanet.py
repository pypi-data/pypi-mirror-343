from typing import List, Dict, Optional, Union, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import re
import pandas as pd
import chardet



class ValveType(Enum):
    PRV = "PRV"  # Pressure Reducing Valve
    PSV = "PSV"  # Pressure Sustaining Valve
    PBV = "PBV"  # Pressure Breaker Valve
    FCV = "FCV"  # Flow Control Valve
    TCV = "TCV"  # Throttle Control Valve
    GPV = "GPV"  # General Purpose Valve


class MixingModel(Enum):
    MIXED = "MIXED"  # Completely mixed
    FIFO = "FIFO"    # First in, first out
    LIFO = "LIFO"    # Last in, first out
    TWOCOMP = "2COMP"  # Two-compartment mixing


class SourceType(Enum):
    CONCEN = "CONCEN"  # Sets the concentration of external inflow
    MASS = "MASS"      # Sets the mass flow rate of external inflow
    SETPOINT = "SETPOINT"  # Sets the concentration leaving the node
    FLOWPACED = "FLOWPACED"  # Adds a flow-weighted increment to the concentration


class Status(Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    CV = "CV"  # Check Valve


@dataclass
class Coordinate:
    x: float
    y: float


@dataclass
class DemandInfo:
    value: float
    pattern: Optional[str] = None
    category: Optional[str] = None


@dataclass
class Node:
    id: str
    x_coord: Optional[float] = None
    y_coord: Optional[float] = None
    tag: Optional[str] = None
    description: Optional[str] = None
    initial_quality: Optional[float] = None

    @property
    def coordinates(self) -> Optional[Coordinate]:
        if self.x_coord is not None and self.y_coord is not None:
            return Coordinate(self.x_coord, self.y_coord)
        return None

    @coordinates.setter
    def coordinates(self, coord: Coordinate):
        self.x_coord = coord.x
        self.y_coord = coord.y


@dataclass
class Junction(Node):
    elevation: float = 0.0
    # Replaced demand and pattern with a list of DemandInfo
    demands: List[DemandInfo] = field(default_factory=list)
    emitter_coeff: Optional[float] = None

    @property
    def base_demand(self) -> Optional[DemandInfo]:
        """Returns the base demand (first in the list), if any."""
        return self.demands[0] if self.demands else None


@dataclass
class Reservoir(Node):
    head: float = 0.0
    pattern: Optional[str] = None


@dataclass
class Tank(Node):
    elevation: float = 0.0
    init_level: float = 0.0
    min_level: float = 0.0
    max_level: float = 0.0
    diameter: float = 0.0
    min_vol: float = 0.0
    vol_curve: Optional[str] = None
    overflow: bool = False
    mixing_model: Optional[MixingModel] = None
    mixing_fraction: Optional[float] = None


@dataclass
class Vertex:
    x: float
    y: float


@dataclass
class Link:
    id: str
    node1: str
    node2: str
    tag: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Union[Status, float]] = Status.OPEN # Allow float for pump speed / valve setting
    vertices: List[Vertex] = field(default_factory=list)


@dataclass
class Pipe(Link):
    length: float = 0.0
    diameter: float = 0.0
    roughness: float = 0.0
    minor_loss: float = 0.0
    bulk_reaction_coeff: Optional[float] = None
    wall_reaction_coeff: Optional[float] = None


@dataclass
class Pump(Link):
    head_curve_id: Optional[str] = None
    power: Optional[float] = None
    speed: float = 1.0 # Default speed is 1.0
    pattern: Optional[str] = None
    efficiency_curve: Optional[str] = None
    efficiency: Optional[float] = None # Added for simple efficiency value
    energy_price: Optional[float] = None
    energy_pattern: Optional[str] = None


@dataclass
class Valve(Link):
    diameter: float = 0.0
    type: Optional[ValveType] = None
    setting: float = 0.0
    minor_loss: float = 0.0


@dataclass
class Source:
    node_id: str
    type: SourceType
    quality: float
    pattern: Optional[str] = None


@dataclass
class Curve:
    id: str
    curve_type: str
    x_values: List[float]
    y_values: List[float]

    def add_point(self, x: float, y: float):
        self.x_values.append(x)
        self.y_values.append(y)


@dataclass
class Pattern:
    id: str
    multipliers: List[float]
    description: Optional[str] = None

    def add_multipliers(self, new_multipliers: List[float]):
        self.multipliers.extend(new_multipliers)


@dataclass
class Control:
    condition: str
    action: str

    def __str__(self):
        return f"LINK {self.action} IF {self.condition}"


@dataclass
class Rule:
    id: str
    conditions: List[str]
    actions: List[str]

    def __str__(self):
        rule_str = f"RULE {self.id}\n"

        for i, condition in enumerate(self.conditions):
            prefix = "IF" if i == 0 else "AND"
            rule_str += f"{prefix} {condition}\n"

        for i, action in enumerate(self.actions):
            prefix = "THEN" if i == 0 else "AND"
            rule_str += f"{prefix} {action}\n"

        return rule_str


@dataclass
class Energy:
    global_efficiency: Optional[float] = None
    global_price: Optional[float] = None
    global_pattern: Optional[str] = None
    demand_charge: Optional[float] = None


@dataclass
class Reaction:
    order_bulk: Optional[int] = None
    order_tank: Optional[int] = None
    order_wall: Optional[int] = None
    global_bulk: Optional[float] = None
    global_wall: Optional[float] = None
    limiting_potential: Optional[float] = None
    roughness_correlation: Optional[float] = None


@dataclass
class Times:
    duration: str = "24:00"
    hydraulic_timestep: str = "1:00"
    quality_timestep: str = "0:05"
    pattern_timestep: str = "1:00"
    pattern_start: str = "0:00"
    report_timestep: str = "1:00"
    report_start: str = "0:00"
    start_clocktime: str = "0:00"
    statistic: str = "NONE"


@dataclass
class Report:
    status: bool = True
    summary: bool = False
    page_size: int = 0
    nodes: List[str] = field(default_factory=lambda: ["ALL"])
    links: List[str] = field(default_factory=lambda: ["ALL"])
    parameters: List[str] = field(default_factory=list)


@dataclass
class Options:
    units: str = "LPS"
    headloss: str = "D-W"
    specific_gravity: float = 1.0
    viscosity: float = 1.0
    trials: int = 40
    accuracy: float = 0.001
    check_freq: int = 2
    max_check: int = 10
    damp_limit: float = 0.0
    unbalanced: str = "Continue 10"
    pattern: Optional[str] = None # Made Optional
    demand_multiplier: float = 1.0
    emitter_exponent: float = 0.5
    quality: Optional[str] = "CHEMICAL mg/L" # Made Optional
    diffusivity: float = 1.0
    tolerance: float = 0.01


@dataclass
class Label:
    x: float
    y: float
    text: str
    anchor_node: Optional[str] = None


@dataclass
class Backdrop:
    dimensions: Optional[Tuple[float, float, float, float]] = None  # (x1, y1, x2, y2)
    units: Optional[str] = None
    file: Optional[str] = None
    offset: Optional[Tuple[float, float]] = None  # (x, y)


class EPANETNetwork:
    """Represents an EPANET network."""
    def __init__(self, title: str = "EPANET Network"):
        self.title = title
        self.source_encoding: Optional[str] = None
        self.junctions: Dict[str, Junction] = {}
        self.reservoirs: Dict[str, Reservoir] = {}
        self.tanks: Dict[str, Tank] = {}
        self.pipes: Dict[str, Pipe] = {}
        self.pumps: Dict[str, Pump] = {}
        self.valves: Dict[str, Valve] = {}

        self.patterns: Dict[str, Pattern] = {}
        self.curves: Dict[str, Curve] = {}
        self.controls: List[Control] = []
        self.rules: Dict[str, Rule] = {}
        self.sources: Dict[str, Source] = {}
        self.labels: List[Label] = []

        self.energy = Energy()
        self.reaction = Reaction()
        self.times = Times()
        self.report = Report()
        self.options = Options()
        self.backdrop = Backdrop()

    def get_all_nodes(self) -> Dict[str, Node]:
        all_nodes = {}
        all_nodes.update(self.junctions)
        all_nodes.update(self.reservoirs)
        all_nodes.update(self.tanks)
        return all_nodes

    def get_all_links(self) -> Dict[str, Link]:
        all_links = {}
        all_links.update(self.pipes)
        all_links.update(self.pumps)
        all_links.update(self.valves)
        return all_links

    def get_node_by_id(self, node_id: str) -> Optional[Node]:
        all_nodes = self.get_all_nodes()
        return all_nodes.get(node_id)

    def get_link_by_id(self, link_id: str) -> Optional[Link]:
        all_links = self.get_all_links()
        return all_links.get(link_id)

    def change_node_id(self, old_node_id: str, new_node_id: str) -> bool:
        node_to_modify = self.get_node_by_id(old_node_id)

        if not node_to_modify:
            return False

        if old_node_id == new_node_id:
            return True

        if self.get_node_by_id(new_node_id):
            return False


        old_id_pattern = re.compile(r'\b' + re.escape(old_node_id) + r'\b')

        # 1. Update references in Links (Pipes, Pumps, Valves)
        all_links = self.get_all_links()
        for link in all_links.values():
            if link.node1 == old_node_id:
                link.node1 = new_node_id
            if link.node2 == old_node_id:
                link.node2 = new_node_id

        # 2. Update references in Sources
        if old_node_id in self.sources:
            source_to_modify = self.sources[old_node_id]
            del self.sources[old_node_id] # Remove old key
            source_to_modify.node_id = new_node_id # Update ID on object
            self.sources[new_node_id] = source_to_modify # Add with new key

        # 3. Update references in Labels (anchor_node)
        for label in self.labels:
            if label.anchor_node == old_node_id:
                label.anchor_node = new_node_id

        # 4. Update references in Controls (condition and action strings)
        for control in self.controls:
            control.condition = old_id_pattern.sub(new_node_id, control.condition)
            control.action = old_id_pattern.sub(new_node_id, control.action)

        # 5. Update references in Rules (condition and action strings)
        for rule_id, rule in self.rules.items():
            updated_conditions = []
            for condition in rule.conditions:
                updated_conditions.append(old_id_pattern.sub(new_node_id, condition))
            rule.conditions = updated_conditions

            updated_actions = []
            for action in rule.actions:
                updated_actions.append(old_id_pattern.sub(new_node_id, action))
            rule.actions = updated_actions

        # 6. Update the Node object itself and its key in the appropriate dictionary
        if isinstance(node_to_modify, Junction):
            del self.junctions[old_node_id]
            node_to_modify.id = new_node_id
            self.junctions[new_node_id] = node_to_modify
        elif isinstance(node_to_modify, Reservoir):
            del self.reservoirs[old_node_id]
            node_to_modify.id = new_node_id
            self.reservoirs[new_node_id] = node_to_modify
        elif isinstance(node_to_modify, Tank):
            del self.tanks[old_node_id]
            node_to_modify.id = new_node_id
            self.tanks[new_node_id] = node_to_modify

        return True

    def add_junction(self, junction: Junction):
        if junction.id in self.get_all_nodes():
            return
        self.junctions[junction.id] = junction

    def add_reservoir(self, reservoir: Reservoir):
        if reservoir.id in self.get_all_nodes():
            return
        self.reservoirs[reservoir.id] = reservoir

    def add_tank(self, tank: Tank):
        if tank.id in self.get_all_nodes():
            return
        self.tanks[tank.id] = tank

    def add_pipe(self, pipe: Pipe):
        if pipe.id in self.get_all_links():
            return
        self.pipes[pipe.id] = pipe

    def add_pump(self, pump: Pump):
        if pump.id in self.get_all_links():
            return
        self.pumps[pump.id] = pump

    def add_valve(self, valve: Valve):
        if valve.id in self.get_all_links():
            return
        self.valves[valve.id] = valve

    def add_pattern(self, pattern: Pattern):
        if pattern.id in self.patterns:
             # Allow appending multipliers if pattern exists
             existing_pattern = self.patterns[pattern.id]
             existing_pattern.add_multipliers(pattern.multipliers)
             if pattern.description and not existing_pattern.description:
                 existing_pattern.description = pattern.description
        else:
            self.patterns[pattern.id] = pattern

    def add_curve(self, curve: Curve):
        if curve.id in self.curves:
             # Allow adding points if curve exists
             existing_curve = self.curves[curve.id]
             for x, y in zip(curve.x_values, curve.y_values):
                 existing_curve.add_point(x, y)
        else:
             self.curves[curve.id] = curve

    def add_control(self, control: Control):
        self.controls.append(control)

    def add_rule(self, rule: Rule):
        if rule.id in self.rules:
            return
        self.rules[rule.id] = rule

    def add_source(self, source: Source):
        self.sources[source.node_id] = source # Overwrite if exists

    def add_label(self, label: Label):
        self.labels.append(label)


class EPANETReader:
    """Class for reading EPANET .inp files into an EPANETNetwork object"""

    def __init__(self):
        self.network: Optional[EPANETNetwork] = None
        self.section_parsers = {
            "[TITLE]": self._parse_title,
            "[JUNCTIONS]": self._parse_junctions,
            "[RESERVOIRS]": self._parse_reservoirs,
            "[TANKS]": self._parse_tanks,
            "[PIPES]": self._parse_pipes,
            "[PUMPS]": self._parse_pumps,
            "[VALVES]": self._parse_valves,
            "[TAGS]": self._parse_tags,
            "[DEMANDS]": self._parse_demands,  # Add parser for DEMANDS
            "[STATUS]": self._parse_status,
            "[PATTERNS]": self._parse_patterns,
            "[CURVES]": self._parse_curves,
            "[CONTROLS]": self._parse_controls,
            "[RULES]": self._parse_rules,
            "[ENERGY]": self._parse_energy,
            "[EMITTERS]": self._parse_emitters,
            "[QUALITY]": self._parse_quality,
            "[SOURCES]": self._parse_sources,
            "[REACTIONS]": self._parse_reactions,
            "[MIXING]": self._parse_mixing,
            "[TIMES]": self._parse_times,
            "[REPORT]": self._parse_report,
            "[OPTIONS]": self._parse_options,
            "[COORDINATES]": self._parse_coordinates,
            "[VERTICES]": self._parse_vertices,
            "[LABELS]": self._parse_labels,
            "[BACKDROP]": self._parse_backdrop,
        }

    def read(self, file_path: str) -> EPANETNetwork:
        self.network = EPANETNetwork()
        detected_encoding: Optional[str] = None
        content: str = ""

        try:
            with open(file_path, 'rb') as fb:
                raw_data = fb.read()
                if not raw_data:
                    return self.network

            detection_result: Optional[Dict[str, Any]] = chardet.detect(raw_data)

            if detection_result and detection_result['encoding']:
                detected_encoding = detection_result['encoding']
                self.network.source_encoding = detected_encoding
            else:
                detected_encoding = 'utf-8'
                self.network.source_encoding = None

            with open(file_path, 'r', encoding=detected_encoding, errors='replace') as f:
                content = f.read()

        except FileNotFoundError:
            raise
        except UnicodeDecodeError as e:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                self.network.source_encoding = 'latin-1'
            except Exception as fallback_e:
                raise e
        except Exception as e:
            raise

        sections = self._split_into_sections(content)

        # Important: Parse JUNCTIONS before DEMANDS
        parse_order = [
            "[TITLE]", "[JUNCTIONS]", "[RESERVOIRS]", "[TANKS]",
            "[PIPES]", "[PUMPS]", "[VALVES]", "[EMITTERS]", "[QUALITY]",
            "[DEMANDS]", # Parse DEMANDS after JUNCTIONS
            "[SOURCES]", "[MIXING]", "[REACTIONS]", "[PATTERNS]", "[CURVES]",
            "[STATUS]", "[CONTROLS]", "[RULES]", "[ENERGY]", "[TIMES]",
            "[REPORT]", "[OPTIONS]", "[COORDINATES]", "[VERTICES]",
            "[LABELS]", "[BACKDROP]", "[TAGS]"
        ]

        parsed_sections = set()

        # Parse sections in a defined order to handle dependencies (like JUNCTIONS -> DEMANDS)
        for section_name in parse_order:
            if section_name in sections:
                parser = self.section_parsers.get(section_name)
                if parser:
                    try:
                        parser(sections[section_name])
                        parsed_sections.add(section_name)
                    except Exception as parse_error:
                        # Decide whether to continue or raise
                        pass # Continue for robustness

        # Parse any remaining sections not in the specific order (e.g., custom sections)
        for section_name, section_content in sections.items():
            if section_name not in parsed_sections:
                 parser = self.section_parsers.get(section_name)
                 if parser:
                     try:
                         parser(section_content)
                     except Exception as parse_error:
                         pass # Continue for robustness

        return self.network

    def _split_into_sections(self, content: str) -> Dict[str, str]:
        sections = {}
        current_section = None
        current_content = []

        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip:
                continue

            if line_strip.startswith('[') and line_strip.endswith(']'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)

                current_section = line_strip.upper()
                current_content = []
            elif current_section:
                current_content.append(line) # Keep original line formatting for content

        if current_section:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def _extract_description(self, line: str) -> Tuple[str, Optional[str]]:
        parts = line.split(';', 1)
        data_part = parts[0].rstrip() # Keep spaces before semicolon
        description = parts[1].strip() if len(parts) > 1 else None
        return data_part, description


    def _parse_title(self, content: str):
        if content:
            self.network.title = content.strip() # Title is usually multiline


    def _parse_junctions(self, content: str):
        """Parse the JUNCTIONS section, adding the base demand."""
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]

        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue

            data_part, description = self._extract_description(line)
            parts = data_part.split()

            if len(parts) >= 3:
                junction_id = parts[0]
                elevation = float(parts[1])
                base_demand_val = float(parts[2])
                pattern_id = parts[3] if len(parts) > 3 and parts[3] != ';' else None

                # Create the junction object first
                junction = Junction(
                    id=junction_id,
                    elevation=elevation,
                    description=description
                    # Demands list is initially empty
                )

                # Create the base demand info and add it to the list
                base_demand_info = DemandInfo(value=base_demand_val, pattern=pattern_id)
                junction.demands.append(base_demand_info)

                self.network.add_junction(junction)


    def _parse_reservoirs(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            data_part, description = self._extract_description(line)
            parts = data_part.split()
            if len(parts) >= 2:
                reservoir_id = parts[0]
                head = float(parts[1])
                pattern = parts[2] if len(parts) > 2 and parts[2] != ';' else None
                reservoir = Reservoir(
                    id=reservoir_id, head=head, pattern=pattern, description=description
                )
                self.network.add_reservoir(reservoir)


    def _parse_tanks(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            data_part, description = self._extract_description(line)
            parts = data_part.split()
            if len(parts) >= 6:
                tank_id = parts[0]
                elevation = float(parts[1])
                init_level = float(parts[2])
                min_level = float(parts[3])
                max_level = float(parts[4])
                diameter = float(parts[5])
                min_vol = float(parts[6]) if len(parts) > 6 else 0.0
                vol_curve = parts[7] if len(parts) > 7 and parts[7] != ';' else None
                overflow = False # Default to False
                # Check for 'OVERFLOW' keyword specifically, or check the 9th position if it exists
                if len(parts) > 8:
                    overflow_keyword_idx = -1
                    try:
                       overflow_keyword_idx = parts.index('OVERFLOW') # Find exact keyword
                    except ValueError:
                       # Check the position if keyword not found
                       if len(parts) > 8 and parts[8].upper() == 'YES': # EPANET Manual says 'YES'
                           overflow = True

                tank = Tank(
                    id=tank_id, elevation=elevation, init_level=init_level,
                    min_level=min_level, max_level=max_level, diameter=diameter,
                    min_vol=min_vol, vol_curve=vol_curve, overflow=overflow,
                    description=description
                )
                self.network.add_tank(tank)


    def _parse_pipes(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            data_part, description = self._extract_description(line)
            parts = data_part.split()
            if len(parts) >= 7:
                pipe_id = parts[0]
                node1 = parts[1]
                node2 = parts[2]
                length = float(parts[3])
                diameter = float(parts[4])
                roughness = float(parts[5])
                minor_loss = float(parts[6])
                status_str = parts[7].upper() if len(parts) > 7 and parts[7] != ';' else "OPEN"

                status: Optional[Status] = Status.OPEN # Default
                try:
                    if status_str == "CV": status = Status.CV
                    elif status_str == "CLOSED": status = Status.CLOSED
                    elif status_str == "OPEN": status = Status.OPEN
                    else: status = Status.OPEN # Default if unrecognized string
                except KeyError:
                     status = Status.OPEN # Default

                pipe = Pipe(
                    id=pipe_id, node1=node1, node2=node2, length=length,
                    diameter=diameter, roughness=roughness, minor_loss=minor_loss,
                    status=status, description=description
                )
                self.network.add_pipe(pipe)


    def _parse_pumps(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            data_part, description = self._extract_description(line)
            parts = data_part.split()
            if len(parts) >= 3:
                pump_id = parts[0]
                node1 = parts[1]
                node2 = parts[2]
                params_str = ' '.join(parts[3:]) # Join remaining parts for parsing

                pump = Pump(id=pump_id, node1=node1, node2=node2, description=description)

                # Use regex for flexibility in parameter order and case
                head_match = re.search(r'HEAD\s+(\S+)', params_str, re.IGNORECASE)
                if head_match: pump.head_curve_id = head_match.group(1)

                power_match = re.search(r'POWER\s+([\d\.]+)', params_str, re.IGNORECASE)
                if power_match: pump.power = float(power_match.group(1))

                speed_match = re.search(r'SPEED\s+([\d\.]+)', params_str, re.IGNORECASE)
                if speed_match: pump.speed = float(speed_match.group(1))

                pattern_match = re.search(r'PATTERN\s+(\S+)', params_str, re.IGNORECASE)
                if pattern_match: pump.pattern = pattern_match.group(1)

                # Initial status based on presence of params (usually OPEN unless explicitly set in STATUS)
                pump.status = Status.OPEN

                self.network.add_pump(pump)


    def _parse_valves(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            data_part, description = self._extract_description(line)
            parts = data_part.split()
            if len(parts) >= 6: # ID N1 N2 Dia Type Setting [MinorLoss]
                valve_id = parts[0]
                node1 = parts[1]
                node2 = parts[2]
                diameter = float(parts[3])
                valve_type_str = parts[4].upper()
                setting = float(parts[5])
                minor_loss = float(parts[6]) if len(parts) > 6 else 0.0

                valve_type: Optional[ValveType] = None
                try:
                    valve_type = ValveType[valve_type_str]
                except KeyError:
                    pass # Keep type as None if invalid

                valve = Valve(
                    id=valve_id, node1=node1, node2=node2, diameter=diameter,
                    type=valve_type, setting=setting, minor_loss=minor_loss,
                    description=description, status=Status.OPEN # Default status
                )
                self.network.add_valve(valve)

    def _parse_tags(self, content: str):
        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip or line_strip.startswith(';'): continue
            parts = line_strip.split(maxsplit=2) # Split into 3 parts max
            if len(parts) == 3:
                element_type = parts[0].upper()
                element_id = parts[1]
                tag = parts[2] # Tag can contain spaces

                element = None
                if element_type == "NODE":
                    element = self.network.get_node_by_id(element_id)
                elif element_type == "LINK":
                    element = self.network.get_link_by_id(element_id)

                if element:
                    element.tag = tag

    def _parse_demands(self, content: str):
        """Parse the DEMANDS section, adding additional demands to existing junctions."""
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]

        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue

            # Description is optional and less common here, but handle if present
            data_part, _ = self._extract_description(line) # We don't usually store description per demand item
            parts = data_part.split()

            if len(parts) >= 2:
                junction_id = parts[0]
                demand_val = float(parts[1])
                pattern_id = parts[2] if len(parts) > 2 and parts[2] != ';' else None
                category = parts[3] if len(parts) > 3 and parts[3] != ';' else None

                # Find the junction (should already exist from [JUNCTIONS] section)
                node = self.network.get_node_by_id(junction_id)

                if node and isinstance(node, Junction):
                    # Create the additional demand info and append it
                    additional_demand_info = DemandInfo(
                        value=demand_val,
                        pattern=pattern_id,
                        category=category
                    )
                    node.demands.append(additional_demand_info)
                else:
                    # Handle case where junction doesn't exist (optional: log warning)
                    pass


    def _parse_status(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            parts = line_strip.split()
            if len(parts) >= 2:
                link_id = parts[0]
                status_val = parts[1].upper()

                link = self.network.get_link_by_id(link_id)
                if link:
                    try:
                        # Try parsing as Enum first
                        if status_val == "OPEN": link.status = Status.OPEN
                        elif status_val == "CLOSED": link.status = Status.CLOSED
                        elif status_val == "CV": link.status = Status.CV
                        else:
                            # If not an enum, try parsing as float (for valve setting/pump speed)
                            setting_or_speed = float(status_val)
                            link.status = setting_or_speed # Store the float value

                            # Optionally update the specific attribute if needed immediately
                            if isinstance(link, Pump): link.speed = setting_or_speed
                            elif isinstance(link, Valve): link.setting = setting_or_speed

                    except (ValueError, KeyError):
                        link.status = Status.OPEN # Default on parse error

    def _parse_patterns(self, content: str):
        current_pattern_id = None
        current_multipliers = []
        current_description = None

        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip: continue

            if line_strip.startswith(';'):
                # Could be a description line for the *next* pattern ID definition
                potential_desc = line_strip[1:].strip()
                # Heuristic: if the next non-comment line starts with an ID different from current,
                # assume this comment belongs to that new ID. We handle this below.
                current_description = potential_desc # Store potential description
                continue

            data_part, line_desc = self._extract_description(line)
            parts = data_part.split()
            if not parts: continue

            pattern_id = parts[0]
            multipliers_str = parts[1:]

            # New pattern ID encountered
            if pattern_id != current_pattern_id:
                # If there was a previous pattern being built, finalize it
                if current_pattern_id and current_multipliers:
                    pattern = Pattern(id=current_pattern_id, multipliers=current_multipliers, description=None) # Desc applied below if needed
                    self.network.add_pattern(pattern)

                # Start the new pattern
                current_pattern_id = pattern_id
                current_multipliers = []
                # Apply the stored description if it seems to belong to this new ID
                if current_description:
                     # Check if pattern exists (e.g., from add_pattern in loop)
                     if current_pattern_id in self.network.patterns:
                         if not self.network.patterns[current_pattern_id].description:
                             self.network.patterns[current_pattern_id].description = current_description
                     else:
                         # Will be applied when pattern is created later
                         pass # Description will be used when creating the new pattern object
                else:
                    # Reset description if no comment preceded this line
                    current_description = None


            # Add multipliers for the current pattern ID
            try:
                current_multipliers.extend([float(m) for m in multipliers_str])
            except ValueError:
                pass # Ignore lines that don't parse correctly

            # If this line had its own description, it usually applies to this pattern ID
            if line_desc:
                if current_pattern_id in self.network.patterns:
                     if not self.network.patterns[current_pattern_id].description:
                         self.network.patterns[current_pattern_id].description = line_desc
                else:
                    # Apply description when the pattern is created/finalized
                    current_description = line_desc


        # Add the last pattern after the loop finishes
        if current_pattern_id and current_multipliers:
            # Check if pattern already exists from add_pattern logic inside loop
            if current_pattern_id not in self.network.patterns:
                pattern = Pattern(id=current_pattern_id, multipliers=current_multipliers, description=current_description)
                self.network.add_pattern(pattern)
            else:
                # Pattern exists, maybe only description needs update
                if current_description and not self.network.patterns[current_pattern_id].description:
                     self.network.patterns[current_pattern_id].description = current_description


    def _parse_curves(self, content: str):
        current_curve_id = None
        current_type = "PUMP" # Default type
        current_x = []
        current_y = []

        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip: continue

            if line_strip.startswith(';'):
                # Check for curve type comment
                type_match = re.search(r';\s*(PUMP|EFFICIENCY|VOLUME|HEADLOSS)\b', line_strip, re.IGNORECASE)
                if type_match:
                    current_type = type_match.group(1).upper()
                continue

            data_part, _ = self._extract_description(line)
            parts = data_part.split()
            if len(parts) >= 3:
                curve_id = parts[0]
                try:
                    x_val = float(parts[1])
                    y_val = float(parts[2])
                except ValueError:
                    continue # Skip lines with non-numeric points

                # If new curve ID, finalize previous and start new
                if curve_id != current_curve_id:
                    if current_curve_id and current_x:
                        curve = Curve(id=current_curve_id, curve_type=current_type, x_values=current_x, y_values=current_y)
                        self.network.add_curve(curve) # add_curve handles duplicates by appending points

                    current_curve_id = curve_id
                    current_x = []
                    current_y = []
                    # Reset type based on comments preceding this data line if necessary
                    # (Handled by type_match logic above)


                # Add points to the current curve
                current_x.append(x_val)
                current_y.append(y_val)

        # Add the last curve after the loop
        if current_curve_id and current_x:
            curve = Curve(id=current_curve_id, curve_type=current_type, x_values=current_x, y_values=current_y)
            self.network.add_curve(curve)


    def _parse_controls(self, content: str):
        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip or line_strip.startswith(';'): continue

            # Simple controls often use 'LINK' keyword implicitly
            line_upper = line_strip.upper()
            if line_upper.startswith("LINK"): line_strip = line_strip[4:].strip()

            action_part = ""
            condition_part = ""

            # Split based on 'IF', 'AT CLOCKTIME', 'AT TIME'
            if ' IF ' in line_upper:
                parts = re.split(r'\s+IF\s+', line_strip, maxsplit=1, flags=re.IGNORECASE)
                if len(parts) == 2:
                    action_part = parts[0].strip()
                    condition_part = parts[1].strip()
            elif ' AT CLOCKTIME ' in line_upper:
                parts = re.split(r'\s+AT CLOCKTIME\s+', line_strip, maxsplit=1, flags=re.IGNORECASE)
                if len(parts) == 2:
                    action_part = parts[0].strip()
                    # Reconstruct condition to match EPANET's internal structure better
                    condition_part = f"SYSTEM CLOCKTIME = {parts[1].strip()}" # Example, adjust if needed
            elif ' AT TIME ' in line_upper:
                 parts = re.split(r'\s+AT TIME\s+', line_strip, maxsplit=1, flags=re.IGNORECASE)
                 if len(parts) == 2:
                     action_part = parts[0].strip()
                     condition_part = f"SYSTEM TIME = {parts[1].strip()}" # Example

            if action_part and condition_part:
                # Prepend LINK if not already present in action for consistency?
                if not action_part.upper().startswith("LINK"):
                    action_part = f"LINK {action_part}" # Assuming action always targets a link

                control = Control(condition=condition_part, action=action_part)
                self.network.add_control(control)


    def _parse_rules(self, content: str):
        current_rule: Optional[Rule] = None

        for line in content.splitlines():
            line_strip = line.strip().upper()
            if not line_strip or line_strip.startswith(';'): continue

            original_case_line = line.strip() # Keep original case for content

            if line_strip.startswith('RULE'):
                # Finalize previous rule if exists
                if current_rule:
                    self.network.add_rule(current_rule)

                parts = original_case_line.split(maxsplit=1)
                if len(parts) > 1:
                    rule_id = parts[1]
                    current_rule = Rule(id=rule_id, conditions=[], actions=[])
                else:
                    current_rule = None # Invalid RULE line

            elif current_rule:
                if line_strip.startswith('IF'):
                    condition = original_case_line.split(' ', 1)[1] if ' ' in original_case_line else ""
                    current_rule.conditions.append(condition.strip())
                elif line_strip.startswith('AND') and current_rule.actions: # AND after THEN means another action
                     action = original_case_line.split(' ', 1)[1] if ' ' in original_case_line else ""
                     current_rule.actions.append(action.strip())
                elif line_strip.startswith('AND') and current_rule.conditions and not current_rule.actions: # AND after IF means another condition
                     condition = original_case_line.split(' ', 1)[1] if ' ' in original_case_line else ""
                     current_rule.conditions.append(condition.strip())
                elif line_strip.startswith('THEN'):
                    action = original_case_line.split(' ', 1)[1] if ' ' in original_case_line else ""
                    current_rule.actions.append(action.strip())
                elif line_strip.startswith('PRIORITY'):
                     # Optional: Parse priority if needed
                     pass

        # Add the last rule after the loop
        if current_rule:
            self.network.add_rule(current_rule)


    def _parse_energy(self, content: str):
        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip or line_strip.startswith(';'): continue

            parts = line_strip.split()
            if not parts: continue

            key1 = parts[0].upper()

            if key1 == "GLOBAL" and len(parts) >= 3:
                key2 = parts[1].upper()
                value = parts[2]
                try:
                    if key2 == "EFFICIENCY": self.network.energy.global_efficiency = float(value)
                    elif key2 == "PRICE": self.network.energy.global_price = float(value)
                    elif key2 == "PATTERN": self.network.energy.global_pattern = value
                except ValueError: pass # Ignore parse errors

            elif key1 == "DEMAND" and len(parts) >= 3 and parts[1].upper() == "CHARGE":
                try:
                    self.network.energy.demand_charge = float(parts[2])
                except ValueError: pass

            elif key1 == "PUMP" and len(parts) >= 4:
                pump_id = parts[1]
                key2 = parts[2].upper()
                value = parts[3]
                pump = self.network.get_link_by_id(pump_id)
                if pump and isinstance(pump, Pump):
                    try:
                        if key2 == "EFFICIENCY":
                            # Can be a curve ID (string) or a value (float)
                            try: pump.efficiency = float(value) # Try float first
                            except ValueError: pump.efficiency_curve = value # Assume curve ID if not float
                        elif key2 == "PRICE": pump.energy_price = float(value)
                        elif key2 == "PATTERN": pump.energy_pattern = value
                    except ValueError: pass # Ignore parse errors


    def _parse_emitters(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            parts = line_strip.split()
            if len(parts) >= 2:
                junction_id = parts[0]
                try:
                    coeff = float(parts[1])
                    node = self.network.get_node_by_id(junction_id)
                    if node and isinstance(node, Junction):
                        node.emitter_coeff = coeff
                except ValueError:
                    pass # Ignore non-numeric coefficients


    def _parse_quality(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            parts = line_strip.split()
            if len(parts) >= 2:
                node_id = parts[0]
                try:
                    quality = float(parts[1])
                    node = self.network.get_node_by_id(node_id)
                    if node:
                        node.initial_quality = quality
                except ValueError:
                    pass # Ignore non-numeric quality


    def _parse_sources(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            parts = line_strip.split()
            if len(parts) >= 3:
                node_id = parts[0]
                source_type_str = parts[1].upper()
                try:
                    quality = float(parts[2])
                    pattern = parts[3] if len(parts) > 3 else None
                    source_type = SourceType[source_type_str] # Raises KeyError if invalid
                    source = Source(node_id=node_id, type=source_type, quality=quality, pattern=pattern)
                    self.network.add_source(source)
                except (ValueError, KeyError):
                    pass # Ignore invalid lines


    def _parse_reactions(self, content: str):
        # Mapping for easier attribute setting
        reaction_options = {
            "ORDER BULK": ("reaction", "order_bulk", int),
            "ORDER TANK": ("reaction", "order_tank", int),
            "ORDER WALL": ("reaction", "order_wall", int),
            "GLOBAL BULK": ("reaction", "global_bulk", float),
            "GLOBAL WALL": ("reaction", "global_wall", float),
            "LIMITING POTENTIAL": ("reaction", "limiting_potential", float),
            "ROUGHNESS CORRELATION": ("reaction", "roughness_correlation", float),
        }
        pipe_reactions = {
             "BULK": ("bulk_reaction_coeff", float),
             "WALL": ("wall_reaction_coeff", float),
        }

        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip or line_strip.startswith(';'): continue

            parts = line_strip.split()
            if not parts: continue

            key_part = ""
            value_part = ""
            target_id = None

            # Check for keywords like ORDER, GLOBAL, etc.
            potential_key = parts[0].upper()
            if potential_key in ["ORDER", "GLOBAL", "LIMITING", "ROUGHNESS"]:
                 if len(parts) >= 3:
                     key_part = f"{parts[0].upper()} {parts[1].upper()}"
                     value_part = parts[2]
                 elif len(parts) >=2 and potential_key=="LIMITING" and parts[1].upper()=="POTENTIAL": # Special case
                     key_part = "LIMITING POTENTIAL"
                     value_part = parts[2] if len(parts) > 2 else None
                 elif len(parts) >=2 and potential_key=="ROUGHNESS" and parts[1].upper()=="CORRELATION": # Special case
                     key_part = "ROUGHNESS CORRELATION"
                     value_part = parts[2] if len(parts) > 2 else None

            elif potential_key in ["BULK", "WALL"]: # Pipe-specific coefficients
                 if len(parts) >= 3:
                     key_part = potential_key # Just BULK or WALL
                     target_id = parts[1]
                     value_part = parts[2]

            # Apply the parsed values
            if key_part in reaction_options:
                target_obj_name, attr_name, type_func = reaction_options[key_part]
                target_obj = getattr(self.network, target_obj_name)
                if value_part is not None:
                     try:
                         setattr(target_obj, attr_name, type_func(value_part))
                     except (ValueError, TypeError): pass # Ignore conversion errors
            elif key_part in pipe_reactions and target_id is not None:
                attr_name, type_func = pipe_reactions[key_part]
                pipe = self.network.get_link_by_id(target_id)
                if pipe and isinstance(pipe, Pipe) and value_part is not None:
                     try:
                         setattr(pipe, attr_name, type_func(value_part))
                     except (ValueError, TypeError): pass


    def _parse_mixing(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            parts = line_strip.split()
            if len(parts) >= 2:
                tank_id = parts[0]
                model_str = parts[1].upper()
                fraction = None
                if len(parts) > 2:
                    try: fraction = float(parts[2])
                    except ValueError: pass # Keep fraction None if not parseable

                tank = self.network.get_node_by_id(tank_id)
                if tank and isinstance(tank, Tank):
                    try:
                        # Handle 2COMP -> TWOCOMP for Enum
                        if model_str == "2COMP": model_str = "TWOCOMP"
                        tank.mixing_model = MixingModel[model_str]
                        tank.mixing_fraction = fraction # Assign parsed fraction
                    except KeyError:
                         pass # Ignore invalid mixing models


    def _parse_times(self, content: str):
        # Map keys (lowercase, spaces removed) to attribute names
        time_options = {
            "duration": "duration",
            "hydraulictimestep": "hydraulic_timestep",
            "qualitytimestep": "quality_timestep",
            "patterntimestep": "pattern_timestep",
            "patternstart": "pattern_start",
            "reporttimestep": "report_timestep",
            "reportstart": "report_start",
            "startclocktime": "start_clocktime",
            "statistic": "statistic",
        }
        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip or line_strip.startswith(';'): continue

            parts = line_strip.split(None, 1) # Split into key and value parts
            if len(parts) == 2:
                key = parts[0].lower().replace(" ", "")
                value = parts[1].strip()
                if key in time_options:
                    attr_name = time_options[key]
                    setattr(self.network.times, attr_name, value)


    def _parse_report(self, content: str):
        report_params = {
            "ELEVATION", "DEMAND", "HEAD", "PRESSURE", "QUALITY",
            "LENGTH", "DIAMETER", "FLOW", "VELOCITY", "HEADLOSS",
            "POSITION", # For valves
            "SETTING", # For pumps/valves
            "REACTION", "F-FACTOR", "STATUS", # For links ('STATE' in EPANET GUI, STATUS here)
        }
        report_settings = {
            "STATUS": "status", # YES/NO
            "SUMMARY": "summary", # YES/NO
            "PAGE": "page_size", # Integer
            "FILE": None, # Report to file (not stored directly in obj)
            "NODES": "nodes", # List or ALL
            "LINKS": "links", # List or ALL
        }

        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip or line_strip.startswith(';'): continue

            parts = line_strip.split(None, 1) # Split key/value
            if not parts: continue

            key = parts[0].upper()
            value = parts[1].strip() if len(parts) > 1 else ""

            if key in report_settings:
                attr_name = report_settings[key]
                if attr_name == "status" or attr_name == "summary":
                    setattr(self.network.report, attr_name, value.upper() == "YES")
                elif attr_name == "page_size":
                    try: setattr(self.network.report, attr_name, int(value))
                    except ValueError: pass
                elif attr_name == "nodes" or attr_name == "links":
                    if value.upper() == "ALL":
                        setattr(self.network.report, attr_name, ["ALL"])
                    elif value.upper() == "NONE":
                         setattr(self.network.report, attr_name, [])
                    else:
                         # Store list of specific IDs
                         setattr(self.network.report, attr_name, value.split())
                # Ignore FILE for now
            elif key in report_params:
                if value.upper() == "YES":
                     if key not in self.network.report.parameters:
                         self.network.report.parameters.append(key)
                elif value.upper() == "NO":
                     if key in self.network.report.parameters:
                         self.network.report.parameters.remove(key)


    def _parse_options(self, content: str):
        # Map keys (lowercase, spaces removed) to attribute names and types
        options_map = {
            "units": ("units", str),
            "headloss": ("headloss", str),
            "specificgravity": ("specific_gravity", float),
            "viscosity": ("viscosity", float),
            "trials": ("trials", int),
            "accuracy": ("accuracy", float),
            "checkfreq": ("check_freq", int),
            "maxcheck": ("max_check", int),
            "damplimit": ("damp_limit", float),
            "unbalanced": ("unbalanced", str),
            "pattern": ("pattern", str),
            "demandmultiplier": ("demand_multiplier", float),
            "emitterexponent": ("emitter_exponent", float),
            "quality": ("quality", str),
            "diffusivity": ("diffusivity", float),
            "tolerance": ("tolerance", float),
            "map": (None, None), # Ignore MAP option
        }
        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip or line_strip.startswith(';'): continue

            parts = line_strip.split(None, 1)
            if len(parts) == 2:
                key = parts[0].lower().replace(" ", "")
                value_str = parts[1].strip()

                if key in options_map:
                    attr_name, type_func = options_map[key]
                    if attr_name: # Check if we need to store it (ignore MAP)
                        try:
                            # Handle special case for quality NONE
                            if key == "quality" and value_str.upper() == "NONE":
                                setattr(self.network.options, attr_name, None)
                            # Handle special case for pattern NONE
                            elif key == "pattern" and value_str.upper() == "NONE":
                                 setattr(self.network.options, attr_name, None)
                            else:
                                 setattr(self.network.options, attr_name, type_func(value_str))
                        except (ValueError, TypeError):
                             # Fallback for pattern if it fails type conversion (e.g., was None)
                             if key == "pattern":
                                 setattr(self.network.options, attr_name, value_str if value_str else None)
                             elif key == "quality":
                                  setattr(self.network.options, attr_name, value_str if value_str else None)
                             else:
                                 pass # Ignore other conversion errors


    def _parse_coordinates(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            parts = line_strip.split()
            if len(parts) >= 3:
                node_id = parts[0]
                try:
                    x = float(parts[1])
                    y = float(parts[2])
                    node = self.network.get_node_by_id(node_id)
                    if node:
                        node.x_coord = x
                        node.y_coord = y
                except ValueError:
                    pass # Ignore lines with non-numeric coordinates


    def _parse_vertices(self, content: str):
        lines = [line for line in content.splitlines() if not line.strip().startswith(';')]
        for line in lines:
            line_strip = line.strip()
            if not line_strip: continue
            parts = line_strip.split()
            if len(parts) >= 3:
                link_id = parts[0]
                try:
                    x = float(parts[1])
                    y = float(parts[2])
                    link = self.network.get_link_by_id(link_id)
                    if link:
                        link.vertices.append(Vertex(x=x, y=y))
                except ValueError:
                     pass # Ignore non-numeric vertex coords


    def _parse_labels(self, content: str):
        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip or line_strip.startswith(';'): continue

            # Regex to find coordinates and quoted text, then optional anchor
            # Handles coordinates potentially having decimals
            match = re.match(r'^\s*([\d\.\-]+)\s+([\d\.\-]+)\s+"([^"]*)"(?:\s+(\S+))?\s*$', line_strip)

            if match:
                 try:
                     x = float(match.group(1))
                     y = float(match.group(2))
                     text = match.group(3) # Text within quotes
                     anchor = match.group(4) if match.group(4) else None # Optional anchor node ID

                     label = Label(x=x, y=y, text=text, anchor_node=anchor)
                     self.network.labels.append(label)
                 except ValueError:
                     pass # Ignore if coordinates are not valid floats


    def _parse_backdrop(self, content: str):
        backdrop_options = {
            "DIMENSIONS": ("dimensions", tuple, float),
            "UNITS": ("units", str, None),
            "FILE": ("file", str, None),
            "OFFSET": ("offset", tuple, float),
        }
        for line in content.splitlines():
            line_strip = line.strip()
            if not line_strip or line_strip.startswith(';'): continue

            parts = line_strip.split()
            if not parts: continue

            key = parts[0].upper()

            if key in backdrop_options:
                 attr_name, type_func, item_type_func = backdrop_options[key]
                 values_str = parts[1:]

                 try:
                     if type_func == tuple and len(values_str) > 0:
                         # Convert tuple items to float
                         values = tuple(item_type_func(v) for v in values_str)
                         setattr(self.network.backdrop, attr_name, values)
                     elif type_func == str and len(values_str) > 0:
                          # Join potentially space-separated values (like file paths)
                          setattr(self.network.backdrop, attr_name, ' '.join(values_str))
                 except (ValueError, TypeError):
                      pass # Ignore conversion errors

class EPANETWriter:
    """Class for writing an EPANETNetwork object to an EPANET .inp file"""

    def __init__(self, network: EPANETNetwork):
        self.network = network
        # Define standard column widths for better formatting
        self.col_widths = {
            "id": 16,
            "node": 16,
            "coord": 16,
            "value_med": 12,
            "value_short": 8,
            "text": 15,
        }

    def _format_field(self, value: Any, width_key: str, precision: Optional[int] = None, is_text: bool = False) -> str:
        """Helper to format fields with specific width and precision."""
        width = self.col_widths.get(width_key, 15) # Default width
        if value is None:
            # For text fields like pattern/category, return spaces, for numbers maybe 0?
            # Let's return spaces for consistency to allow empty fields.
             return ' ' * width

        if isinstance(value, float):
            fmt = f"{{:<{width}"
            if precision is not None:
                # Use 'f' for fixed point notation
                fmt += f".{precision}f}}"
            else:
                 # Default float precision if none specified (e.g., 6 decimals)
                 # Let's default to 3 for demands if not specified
                 fmt += ".3f}}" if precision is None else "}}"

            try:
                 # Handle potential negative zero formatting if needed, though less common here
                 val_to_format = value
                 # if abs(value) < 1e-9: val_to_format = 0.0 # Treat very small numbers as zero?
                 return fmt.format(val_to_format)
            except (TypeError, ValueError): # Handle potential format errors
                 return str(value).ljust(width)
        elif isinstance(value, Enum):
             return str(value.value).ljust(width)
        elif is_text: # Specifically for text fields like IDs, patterns, etc.
             # Strip leading/trailing whitespace from text before padding
             return str(value).strip().ljust(width)
        else: # Integers, booleans, other types
             return str(value).ljust(width)


    def write(self, file_path: str, default_encoding: str = 'utf-8'):
        encoding_to_use = self.network.source_encoding if self.network.source_encoding else default_encoding

        try:
            with open(file_path, 'w', encoding=encoding_to_use, errors='replace') as f:
                self._write_title(f)
                self._write_junctions(f)
                self._write_reservoirs(f)
                self._write_tanks(f)
                self._write_pipes(f)
                self._write_pumps(f)
                self._write_valves(f)
                self._write_tags(f)
                self._write_demands(f) # Write DEMANDS section
                self._write_status(f)
                self._write_patterns(f)
                self._write_curves(f)
                self._write_controls(f)
                self._write_rules(f)
                self._write_energy(f)
                self._write_emitters(f)
                self._write_quality(f)
                self._write_sources(f)
                self._write_reactions(f)
                self._write_mixing(f)
                self._write_times(f)
                self._write_report(f)
                self._write_options(f)
                self._write_coordinates(f)
                self._write_vertices(f)
                self._write_labels(f)
                self._write_backdrop(f)

                f.write("\n[END]\n")

        except Exception as e:
            import traceback
            traceback.print_exc()
            raise

    def _write_section_header(self, file, section_name):
        file.write(f"\n[{section_name}]\n")

    def _add_description(self, line, description):
        """Appends description with preceding semicolon, ensuring alignment."""
        # Pad line to a consistent length before adding description? Optional.
        # Simplified: Add tab, semicolon, then description if exists.
        line_with_semicolon = f"{line}\t;"
        if description is not None:
            desc_str = str(description).strip()
            if desc_str:
                return f"{line_with_semicolon} {desc_str}" # Add a space after ;
        return line_with_semicolon


    def _write_title(self, file):
        file.write(f"[TITLE]\n")
        # Write potentially multi-line title
        if self.network.title:
             file.write(f"{self.network.title}\n")


    def _write_junctions(self, file):
        """Write the JUNCTIONS section with base demand."""
        if not self.network.junctions: return
        self._write_section_header(file, "JUNCTIONS")
        # Adjusted header for typical spacing
        file.write(f";{'ID':<16}\t{'Elev':<12}\t{'Demand':<12}\t{'Pattern':<15}\n")
        file.write(";" + "-"*15 + "\t" + "-"*11 + "\t" + "-"*11 + "\t" + "-"*14 + "\n")


        for junc_id, junction in sorted(self.network.junctions.items()):
             base_demand_val = 0.0
             base_pattern_id = None
             # Get the first demand entry as the base demand
             if junction.demands:
                 base_demand_info = junction.demands[0]
                 base_demand_val = base_demand_info.value
                 base_pattern_id = base_demand_info.pattern

             line = (f" {self._format_field(junction.id, 'id', is_text=True)}"
                     f"\t{self._format_field(junction.elevation, 'value_med', 2)}"
                     f"\t{self._format_field(base_demand_val, 'value_med', 3)}") # More precision for demand?

             if base_pattern_id:
                 line += f"\t{self._format_field(base_pattern_id, 'text', is_text=True)}"
             else:
                 line += f"\t{' ' * self.col_widths['text']}" # Add space if no pattern

             line = self._add_description(line, junction.description)
             file.write(f"{line}\n")


    def _write_reservoirs(self, file):
        if not self.network.reservoirs: return
        self._write_section_header(file, "RESERVOIRS")
        file.write(f";{'ID':<16}\t{'Head':<12}\t{'Pattern':<15}\n")
        file.write(";" + "-"*15 + "\t" + "-"*11 + "\t" + "-"*14 + "\n")

        for res_id, reservoir in sorted(self.network.reservoirs.items()):
            line = (f" {self._format_field(reservoir.id, 'id', is_text=True)}"
                    f"\t{self._format_field(reservoir.head, 'value_med', 2)}")
            if reservoir.pattern:
                line += f"\t{self._format_field(reservoir.pattern, 'text', is_text=True)}"
            else:
                line += f"\t{' ' * self.col_widths['text']}"

            line = self._add_description(line, reservoir.description)
            file.write(f"{line}\n")


    def _write_tanks(self, file):
        if not self.network.tanks: return
        self._write_section_header(file, "TANKS")
        file.write(f";{'ID':<16}\t{'Elevation':<12}\t{'InitLevel':<12}\t{'MinLevel':<12}\t{'MaxLevel':<12}\t{'Diameter':<12}\t{'MinVol':<12}\t{'VolCurve':<15}\t{'Overflow'}\n")
        file.write(";" + "-"*15 + "\t" + "-"*11 + "\t" + "-"*11 + "\t" + "-"*11 + "\t" + "-"*11 + "\t" + "-"*11 + "\t" + "-"*11 + "\t" + "-"*14 + "\t" + "-"*8 + "\n")

        for tank_id, tank in sorted(self.network.tanks.items()):
            line = (f" {self._format_field(tank.id, 'id', is_text=True)}"
                    f"\t{self._format_field(tank.elevation, 'value_med', 2)}"
                    f"\t{self._format_field(tank.init_level, 'value_med', 2)}"
                    f"\t{self._format_field(tank.min_level, 'value_med', 2)}"
                    f"\t{self._format_field(tank.max_level, 'value_med', 2)}"
                    f"\t{self._format_field(tank.diameter, 'value_med', 2)}"
                    f"\t{self._format_field(tank.min_vol, 'value_med', 2)}")

            if tank.vol_curve:
                line += f"\t{self._format_field(tank.vol_curve, 'text', is_text=True)}"
            else:
                line += f"\t{' ' * self.col_widths['text']}" # Add space if no curve

            if tank.overflow: # EPANET uses 'YES' for overflow flag when present
                 line += "\tYes"
            # Otherwise, omit the overflow field

            line = self._add_description(line, tank.description)
            file.write(f"{line}\n")


    def _write_pipes(self, file):
        if not self.network.pipes: return
        self._write_section_header(file, "PIPES")
        file.write(f";{'ID':<16}\t{'Node1':<16}\t{'Node2':<16}\t{'Length':<12}\t{'Diameter':<12}\t{'Roughness':<12}\t{'MinorLoss':<12}\t{'Status':<8}\n")
        file.write(";" + "-"*15 + "\t" + "-"*15 + "\t" + "-"*15 + "\t" + "-"*11 + "\t" + "-"*11 + "\t" + "-"*11 + "\t" + "-"*11 + "\t" + "-"*7 + "\n")

        for pipe_id, pipe in sorted(self.network.pipes.items()):
             status_to_write = Status.OPEN # Default
             if isinstance(pipe.status, Status):
                 status_to_write = pipe.status

             line = (f" {self._format_field(pipe.id, 'id', is_text=True)}"
                     f"\t{self._format_field(pipe.node1, 'node', is_text=True)}"
                     f"\t{self._format_field(pipe.node2, 'node', is_text=True)}"
                     f"\t{self._format_field(pipe.length, 'value_med', 2)}"
                     f"\t{self._format_field(pipe.diameter, 'value_med', 2)}"
                     f"\t{self._format_field(pipe.roughness, 'value_med', 4)}" # Roughness often has more decimals
                     f"\t{self._format_field(pipe.minor_loss, 'value_med', 3)}"
                     f"\t{self._format_field(status_to_write, 'value_short')}")

             line = self._add_description(line, pipe.description)
             file.write(f"{line}\n")

    def _write_pumps(self, file):
        if not self.network.pumps: return
        self._write_section_header(file, "PUMPS")
        file.write(f";{'ID':<16}\t{'Node1':<16}\t{'Node2':<16}\t{'Parameters'}\n")
        file.write(";" + "-"*15 + "\t" + "-"*15 + "\t" + "-"*15 + "\t" + "-"*20 + "\n")

        for pump_id, pump in sorted(self.network.pumps.items()):
            line = (f" {self._format_field(pump.id, 'id', is_text=True)}"
                    f"\t{self._format_field(pump.node1, 'node', is_text=True)}"
                    f"\t{self._format_field(pump.node2, 'node', is_text=True)}")

            params = []
            if pump.power is not None:
                 params.append(f"POWER {pump.power}")
            elif pump.head_curve_id: # EPANET usually expects HEAD or POWER, HEAD takes precedence if both defined?
                 params.append(f"HEAD {pump.head_curve_id}")
            # Speed and Pattern are optional additions
            if pump.speed is not None and pump.speed != 1.0: # Only write non-default speed
                 params.append(f"SPEED {pump.speed:.2f}") # Format speed
            if pump.pattern:
                 params.append(f"PATTERN {pump.pattern}")

            line += f"\t{' '.join(params)}" # Join params with space
            line = self._add_description(line, pump.description)
            file.write(f"{line}\n")

    def _write_valves(self, file):
        if not self.network.valves: return
        self._write_section_header(file, "VALVES")
        file.write(f";{'ID':<16}\t{'Node1':<16}\t{'Node2':<16}\t{'Diameter':<12}\t{'Type':<5}\t{'Setting':<12}\t{'MinorLoss':<12}\n")
        file.write(";" + "-"*15 + "\t" + "-"*15 + "\t" + "-"*15 + "\t" + "-"*11 + "\t" + "----" + "\t" + "-"*11 + "\t" + "-"*11 + "\n")

        for valve_id, valve in sorted(self.network.valves.items()):
             valve_type_str = "GPV" # Default if type is None
             if isinstance(valve.type, ValveType):
                 valve_type_str = valve.type.value

             line = (f" {self._format_field(valve.id, 'id', is_text=True)}"
                     f"\t{self._format_field(valve.node1, 'node', is_text=True)}"
                     f"\t{self._format_field(valve.node2, 'node', is_text=True)}"
                     f"\t{self._format_field(valve.diameter, 'value_med', 2)}"
                     f"\t{valve_type_str:<5}" # Fixed width for type
                     f"\t{self._format_field(valve.setting, 'value_med', 2)}"
                     f"\t{self._format_field(valve.minor_loss, 'value_med', 3)}")

             line = self._add_description(line, valve.description)
             file.write(f"{line}\n")

    def _write_tags(self, file):
        node_tags = [(node.id, node.tag) for node in self.network.get_all_nodes().values() if node.tag]
        link_tags = [(link.id, link.tag) for link in self.network.get_all_links().values() if link.tag]

        if not node_tags and not link_tags: return
        self._write_section_header(file, "TAGS")
        file.write(f";{'Element':<8}\t{'ID':<16}\t{'Tag'}\n")
        file.write(";" + "-"*7 + "\t" + "-"*15 + "\t" + "-"*20 + "\n")

        for node_id, tag in sorted(node_tags):
            file.write(f" NODE    \t{self._format_field(node_id, 'id', is_text=True)}\t{tag}\n")
        for link_id, tag in sorted(link_tags):
            file.write(f" LINK    \t{self._format_field(link_id, 'id', is_text=True)}\t{tag}\n")

    # Inside class EPANETWriter in epanet.py

    def _write_demands(self, file):
        """Write the DEMANDS section. Now writes ALL demands if count > 1."""
       
        junctions_with_any_demands = [
            j for j in self.network.junctions.values() if j.demands
        ]

      
        any_demands_to_write_here = any(len(j.demands) > 0 for j in self.network.junctions.values())


        if not any_demands_to_write_here:
             # If no junction has any demands in the list (unlikely but possible), skip.
             # Or, if we strictly only wanted additional demands here, check len(j.demands) > 1
             return 

        self._write_section_header(file, "DEMANDS")
        # Use slightly wider Category field?
        file.write(f";{'Junction':<16}\t{'Demand':<12}\t{'Pattern':<15}\t{'Category':<20}\n") 
        file.write(";" + "-"*15 + "\t" + "-"*11 + "\t" + "-"*14 + "\t" + "-"*19 + "\n")

        # Iterate through ALL junctions that have demands specified
        for junction in sorted(junctions_with_any_demands, key=lambda j: j.id):
            # Iterate through ALL demands for that junction
            for i, demand_info in enumerate(junction.demands):
                # -------------------------------------------------------
                # ----> REMOVED THIS BLOCK: <----
                # if i == 0:
                #    continue # OLD: Skip the base demand
                # NOW: Process ALL demands here (including index 0)
                # -------------------------------------------------------

                # Formatting logic remains the same
                line = (f" {self._format_field(junction.id, 'id', is_text=True)}"
                        f"\t{self._format_field(demand_info.value, 'value_med', 3)}")

                if demand_info.pattern:
                    line += f"\t{self._format_field(demand_info.pattern, 'text', is_text=True)}"
                else:
                    line += f"\t{' ' * self.col_widths['text']}" # Use defined width

                if demand_info.category:
                    category_clean = str(demand_info.category).replace(';', '')
                    # Ensure category width matches header comment if needed
                    line += f"\t{self._format_field(category_clean, 'text', is_text=True)}" 
                else:
                     line += f"\t{' ' * self.col_widths.get('text', 20)}" # Use text width, default 20? Match header

                line = self._add_description(line, None) # No description per demand line usually
                file.write(f"{line}\n")


    def _write_status(self, file):
        status_changes = []
        default_pipe_status = Status.OPEN
        default_pump_status = Status.OPEN
        default_valve_status = Status.OPEN # Or based on type? GPV/TCV often Open, others Closed? Assume OPEN default.

        all_links = sorted(self.network.get_all_links().items())

        for link_id, link in all_links:
            status_to_write = None
            is_default = False

            if isinstance(link, Pipe):
                 if isinstance(link.status, Status) and link.status != default_pipe_status:
                     status_to_write = link.status.value
                 # Pipes don't usually have numeric status in [STATUS]
            elif isinstance(link, Pump):
                 # Pumps can be OPEN/CLOSED or have speed setting
                 if isinstance(link.status, Status) and link.status != default_pump_status:
                     status_to_write = link.status.value
                 elif isinstance(link.status, (float, int)) and link.speed != float(link.status):
                      # If status field has a different speed than the main speed attribute? Prioritize status?
                      status_to_write = f"{link.status:.2f}" # Write speed from status field
                 elif isinstance(link.status, (float, int)):
                      status_to_write = f"{link.status:.2f}" # Write speed from status field
                 elif link.speed != 1.0 : # Check speed attribute if status is default Enum
                      status_to_write = f"{link.speed:.2f}"
                 else: # Status is default enum, speed is default 1.0
                     is_default = True
            elif isinstance(link, Valve):
                 # Valves can be OPEN/CLOSED or have setting
                 if isinstance(link.status, Status) and link.status != default_valve_status:
                      status_to_write = link.status.value
                 elif isinstance(link.status, (float, int)) and link.setting != float(link.status):
                       # Status field has different setting? Prioritize status?
                       status_to_write = f"{link.status:.2f}" # Write setting from status field
                 elif isinstance(link.status, (float, int)):
                       status_to_write = f"{link.status:.2f}" # Write setting from status field
                 elif Valve.type not in [ValveType.GPV, ValveType.TCV]: # Some valves default to a setting
                     # Write setting if valve type usually requires one and status is default OPEN
                     status_to_write = f"{link.setting:.2f}"
                 else: # Status is default enum, setting is default 0.0 (or type doesn't need it)
                     is_default = True


            if status_to_write is not None and not is_default:
                status_changes.append((link_id, status_to_write))

        if not status_changes: return # Only write section if there are non-default states
        self._write_section_header(file, "STATUS")
        file.write(f";{'ID':<16}\t{'Status/Setting'}\n")
        file.write(";" + "-"*15 + "\t" + "-"*15 + "\n")

        for link_id, status_value in status_changes:
             file.write(f" {self._format_field(link_id, 'id', is_text=True)}\t{status_value}\n")


    def _write_patterns(self, file):
        if not self.network.patterns: return
        self._write_section_header(file, "PATTERNS")
        file.write(f";{'ID':<16}\t{'Multipliers (max 6 per line)'}\n")
        file.write(";" + "-"*15 + "\t" + "-"*30 + "\n")

        for pattern_id, pattern in sorted(self.network.patterns.items()):
            if pattern.description:
                 # Write description as a comment line before the pattern data
                 file.write(f"; Pattern {pattern.id}: {pattern.description}\n")

            multipliers = pattern.multipliers
            # EPANET typically writes 6 multipliers per line
            for i in range(0, len(multipliers), 6):
                 chunk = multipliers[i:i+6]
                 line = f" {self._format_field(pattern.id, 'id', is_text=True)}"
                 for mult in chunk:
                      # Use a consistent format for multipliers
                      line += f"\t{self._format_field(mult, 'value_med', 3)}"
                 file.write(f"{line}\n")


    def _write_curves(self, file):
        if not self.network.curves: return
        self._write_section_header(file, "CURVES")
        file.write(f";{'ID':<16}\t{'X-Value':<12}\t{'Y-Value':<12}\t; Type: (auto-detected or specify)\n")
        file.write(";" + "-"*15 + "\t" + "-"*11 + "\t" + "-"*11 + "\n")

        # Group curves by ID to write them contiguously
        curves_sorted = sorted(self.network.curves.items())

        for curve_id, curve in curves_sorted:
             # Optional: Write curve type as comment if needed
             # file.write(f"; Curve {curve.id} Type: {curve.curve_type}\n")
             for i in range(len(curve.x_values)):
                  line = (f" {self._format_field(curve.id, 'id', is_text=True)}"
                          f"\t{self._format_field(curve.x_values[i], 'value_med', 3)}"
                          f"\t{self._format_field(curve.y_values[i], 'value_med', 3)}")
                  file.write(f"{line}\n")


    def _write_controls(self, file):
        if not self.network.controls: return
        self._write_section_header(file, "CONTROLS")
        file.write("; Simple Controls (add LINK/SYSTEM prefixes if needed)\n")

        for control in self.network.controls:
             # Format based on common EPANET control structures
             action = control.action.upper().replace("LINK ", "").strip() # Simplify action part
             condition = control.condition.strip()

             # Reconstruct common formats
             time_match = re.match(r'SYSTEM\s+TIME\s*([=<>]+)\s*(\S+)', condition, re.IGNORECASE)
             clock_match = re.match(r'SYSTEM\s+CLOCKTIME\s*([=<>]+)\s*(\S+)', condition, re.IGNORECASE)
             node_match = re.match(r'NODE\s+(\S+)\s+(PRESSURE|HEAD)\s*([=<>]+)\s*([\d\.\-]+)', condition, re.IGNORECASE)
             link_match = re.match(r'LINK\s+(\S+)\s+STATUS\s*IS\s+(OPEN|CLOSED)', condition, re.IGNORECASE) # Example


             if clock_match:
                 # Use 'AT CLOCKTIME' format
                 # Note: EPANET only supports '=' for clocktime triggers, implicitly
                 time_val = clock_match.group(2)
                 file.write(f" LINK {action} AT CLOCKTIME {time_val}\n")
             elif time_match:
                  # Use 'AT TIME' format
                  time_val = time_match.group(2)
                  file.write(f" LINK {action} AT TIME {time_val}\n")
             elif node_match or link_match: # Other conditional controls use IF
                  file.write(f" LINK {action} IF {condition}\n")
             else: # Default fallback IF format
                 file.write(f" LINK {action} IF {condition}\n")


    def _write_rules(self, file):
        if not self.network.rules: return
        self._write_section_header(file, "RULES")

        for rule_id, rule in sorted(self.network.rules.items()):
            file.write(f"RULE {rule.id}\n")
            for i, condition in enumerate(rule.conditions):
                prefix = "IF" if i == 0 else "AND"
                file.write(f" {prefix:<3} {condition}\n") # Align IF/AND
            for i, action in enumerate(rule.actions):
                prefix = "THEN" if i == 0 else "AND"
                file.write(f" {prefix:<3} {action}\n") # Align THEN/AND
            # Priority not currently stored/written
            file.write("\n") # Blank line between rules


    def _write_energy(self, file):
        r = self.network.energy
        pump_energy = [
            (pid, p) for pid, p in self.network.pumps.items()
            if p.efficiency_curve is not None or p.efficiency is not None or p.energy_price is not None or p.energy_pattern is not None
        ]
        has_energy = (r.global_efficiency is not None or r.global_price is not None or
                      r.global_pattern is not None or r.demand_charge is not None or
                      bool(pump_energy))

        if not has_energy: return
        self._write_section_header(file, "ENERGY")

        if r.global_efficiency is not None: file.write(f" Global Efficiency\t{r.global_efficiency}\n")
        if r.global_price is not None: file.write(f" Global Price     \t{r.global_price}\n")
        if r.global_pattern is not None: file.write(f" Global Pattern   \t{r.global_pattern}\n")
        if r.demand_charge is not None: file.write(f" Demand Charge    \t{r.demand_charge}\n")

        for pump_id, pump in sorted(pump_energy):
            pump_id_f = self._format_field(pump_id, 'id', is_text=True)
            if pump.efficiency is not None: # Write direct efficiency if available
                 file.write(f" Pump {pump_id_f}\tEfficiency\t{pump.efficiency}\n")
            elif pump.efficiency_curve is not None: # Write curve ID otherwise
                 file.write(f" Pump {pump_id_f}\tEfficiency\t{pump.efficiency_curve}\n")

            if pump.energy_price is not None:
                 file.write(f" Pump {pump_id_f}\tPrice     \t{pump.energy_price}\n")
            if pump.energy_pattern is not None:
                 file.write(f" Pump {pump_id_f}\tPattern   \t{pump.energy_pattern}\n")


    def _write_emitters(self, file):
        emitters = sorted([(j.id, j.emitter_coeff) for j in self.network.junctions.values() if j.emitter_coeff is not None])
        if not emitters: return
        self._write_section_header(file, "EMITTERS")
        file.write(f";{'Junction':<16}\t{'Coefficient':<12}\n")
        file.write(";" + "-"*15 + "\t" + "-"*11 + "\n")

        for junction_id, coeff in emitters:
            line = (f" {self._format_field(junction_id, 'id', is_text=True)}"
                    f"\t{self._format_field(coeff, 'value_med', 4)}") # More precision for emitters?
            file.write(f"{line}\n")


    def _write_quality(self, file):
        quality_nodes = sorted([(n.id, n.initial_quality) for n in self.network.get_all_nodes().values() if n.initial_quality is not None])
        if not quality_nodes: return
        self._write_section_header(file, "QUALITY")
        file.write(f";{'Node':<16}\t{'InitQual':<12}\n")
        file.write(";" + "-"*15 + "\t" + "-"*11 + "\n")

        for node_id, quality in quality_nodes:
            line = (f" {self._format_field(node_id, 'id', is_text=True)}"
                    f"\t{self._format_field(quality, 'value_med', 3)}")
            file.write(f"{line}\n")


    def _write_sources(self, file):
        if not self.network.sources: return
        self._write_section_header(file, "SOURCES")
        file.write(f";{'Node':<16}\t{'Type':<10}\t{'Quality':<12}\t{'Pattern':<15}\n")
        file.write(";" + "-"*15 + "\t" + "-"*9 + "\t" + "-"*11 + "\t" + "-"*14 + "\n")

        for source_id, source in sorted(self.network.sources.items()):
             source_type_str = source.type.value if isinstance(source.type, SourceType) else "CONCEN"
             line = (f" {self._format_field(source.node_id, 'id', is_text=True)}"
                     f"\t{source_type_str:<10}"
                     f"\t{self._format_field(source.quality, 'value_med', 3)}")
             if source.pattern:
                 line += f"\t{self._format_field(source.pattern, 'text', is_text=True)}"
             # No else needed, omit if None

             file.write(f"{line}\n")


    def _write_reactions(self, file):
        r = self.network.reaction
        pipe_reactions_bulk = sorted([(p.id, p.bulk_reaction_coeff) for p in self.network.pipes.values() if p.bulk_reaction_coeff is not None])
        pipe_reactions_wall = sorted([(p.id, p.wall_reaction_coeff) for p in self.network.pipes.values() if p.wall_reaction_coeff is not None])

        has_reactions = (r.order_bulk is not None or r.order_tank is not None or r.order_wall is not None or
                         r.global_bulk is not None or r.global_wall is not None or
                         r.limiting_potential is not None or r.roughness_correlation is not None or
                         bool(pipe_reactions_bulk) or bool(pipe_reactions_wall))

        if not has_reactions: return
        self._write_section_header(file, "REACTIONS")
        # Use fixed spacing for keywords
        kw_width = 20
        if r.order_bulk is not None: file.write(f" {'Order Bulk':<{kw_width}}\t{r.order_bulk}\n")
        if r.order_tank is not None: file.write(f" {'Order Tank':<{kw_width}}\t{r.order_tank}\n")
        if r.order_wall is not None: file.write(f" {'Order Wall':<{kw_width}}\t{r.order_wall}\n")
        if r.global_bulk is not None: file.write(f" {'Global Bulk':<{kw_width}}\t{r.global_bulk}\n")
        if r.global_wall is not None: file.write(f" {'Global Wall':<{kw_width}}\t{r.global_wall}\n")
        if r.limiting_potential is not None: file.write(f" {'Limiting Potential':<{kw_width}}\t{r.limiting_potential}\n")
        if r.roughness_correlation is not None: file.write(f" {'Roughness Correlation':<{kw_width}}\t{r.roughness_correlation}\n")

        # Pipe specific coefficients
        for pipe_id, coeff in pipe_reactions_bulk:
            pipe_id_f = self._format_field(pipe_id, 'id', is_text=True)
            file.write(f" {'Bulk':<8}{pipe_id_f}\t{coeff}\n") # Shorter keyword width here
        for pipe_id, coeff in pipe_reactions_wall:
            pipe_id_f = self._format_field(pipe_id, 'id', is_text=True)
            file.write(f" {'Wall':<8}{pipe_id_f}\t{coeff}\n")


    def _write_mixing(self, file):
        mixing_tanks = sorted([
            (t.id, t.mixing_model, t.mixing_fraction)
            for t in self.network.tanks.values() if t.mixing_model is not None
        ])
        if not mixing_tanks: return
        self._write_section_header(file, "MIXING")
        file.write(f";{'Tank ID':<16}\t{'Model':<8}\t{'Fraction':<12}\n")
        file.write(";" + "-"*15 + "\t" + "-"*7 + "\t" + "-"*11 + "\n")

        for tank_id, model, fraction in mixing_tanks:
            model_str = "MIXED" # Default
            if isinstance(model, MixingModel):
                 model_str = model.value.replace("TWOCOMP", "2COMP") # Use 2COMP in output

            line = (f" {self._format_field(tank_id, 'id', is_text=True)}"
                    f"\t{model_str:<8}") # Fixed width for model

            if model == MixingModel.TWOCOMP and fraction is not None:
                line += f"\t{self._format_field(fraction, 'value_med', 3)}"
            # Omit fraction for other models or if None

            file.write(f"{line}\n")


    def _write_times(self, file):
        self._write_section_header(file, "TIMES")
        t = self.network.times
        kw_width = 20 # Keyword width
        file.write(f" {'Duration':<{kw_width}}\t{t.duration}\n")
        file.write(f" {'Hydraulic Timestep':<{kw_width}}\t{t.hydraulic_timestep}\n")
        file.write(f" {'Quality Timestep':<{kw_width}}\t{t.quality_timestep}\n")
        # Only write non-default values for the rest? Or write all? EPANET writes all.
        file.write(f" {'Pattern Timestep':<{kw_width}}\t{t.pattern_timestep}\n")
        file.write(f" {'Pattern Start':<{kw_width}}\t{t.pattern_start}\n")
        file.write(f" {'Report Timestep':<{kw_width}}\t{t.report_timestep}\n")
        file.write(f" {'Report Start':<{kw_width}}\t{t.report_start}\n")
        file.write(f" {'Start ClockTime':<{kw_width}}\t{t.start_clocktime}\n")
        file.write(f" {'Statistic':<{kw_width}}\t{t.statistic}\n")


    def _write_report(self, file):
        self._write_section_header(file, "REPORT")
        r = self.network.report
        kw_width = 15

        # --- Write Parameters First ---
        param_lines = []
        # Define standard order if desired
        all_params_ordered = [
             "Demand", "Head", "Pressure", "Quality", # Node params
             "Flow", "Velocity", "Headloss", "Quality", # Link params (Quality repeated okay)
             "Status", "Setting", "Reaction", "F-Factor" # Link params
        ]
        # Add others not in standard list?
        all_params_set = set(all_params_ordered) | set(r.parameters)

        params_to_write = {p: False for p in all_params_set if p} # Initialize all potential params to NO
        for p in r.parameters:
            if p: params_to_write[p] = True # Set YES for params present in the list

        if any(params_to_write.values()): file.write("; Parameters Reported (YES/NO)\n")
        for param in sorted(params_to_write.keys()): # Write all known params in alphabetical order
            file.write(f" {param:<{kw_width}}\t{'YES' if params_to_write[param] else 'NO'}\n")

        # --- Write Report Settings ---
        file.write("\n; Report Settings\n")
        if r.nodes == ["ALL"]:
             file.write(f" {'Nodes':<{kw_width}}\tALL\n")
        elif not r.nodes: # Empty list means NONE
             file.write(f" {'Nodes':<{kw_width}}\tNONE\n")
        else:
             file.write(f" {'Nodes':<{kw_width}}\t{' '.join(r.nodes)}\n")

        if r.links == ["ALL"]:
             file.write(f" {'Links':<{kw_width}}\tALL\n")
        elif not r.links: # Empty list means NONE
            file.write(f" {'Links':<{kw_width}}\tNONE\n")
        else:
            file.write(f" {'Links':<{kw_width}}\t{' '.join(r.links)}\n")


        file.write(f" {'Status':<{kw_width}}\t{'YES' if r.status else 'NO'}\n")
        file.write(f" {'Summary':<{kw_width}}\t{'YES' if r.summary else 'NO'}\n")
        if r.page_size > 0: file.write(f" {'Page':<{kw_width}}\t{r.page_size}\n")
        # Report File not written here

    def _write_options(self, file):
        self._write_section_header(file, "OPTIONS")
        o = self.network.options
        kw_width = 18 # Keyword width

        file.write(f" {'Units':<{kw_width}}\t{o.units}\n")
        file.write(f" {'Headloss':<{kw_width}}\t{o.headloss}\n")
        file.write(f" {'Specific Gravity':<{kw_width}}\t{o.specific_gravity}\n")
        file.write(f" {'Viscosity':<{kw_width}}\t{o.viscosity}\n")
        file.write(f" {'Trials':<{kw_width}}\t{o.trials}\n")
        file.write(f" {'Accuracy':<{kw_width}}\t{o.accuracy}\n")
        file.write(f" {'Unbalanced':<{kw_width}}\t{o.unbalanced}\n")

        if o.pattern is not None:
            file.write(f" {'Pattern':<{kw_width}}\t{o.pattern}\n")
        else: # Write NONE if pattern is None
            file.write(f" {'Pattern':<{kw_width}}\tNONE\n")

        file.write(f" {'Demand Multiplier':<{kw_width}}\t{o.demand_multiplier}\n")
        file.write(f" {'Emitter Exponent':<{kw_width}}\t{o.emitter_exponent}\n")

        if o.quality is not None:
            file.write(f" {'Quality':<{kw_width}}\t{o.quality}\n")
            file.write(f" {'Diffusivity':<{kw_width}}\t{o.diffusivity}\n")
            file.write(f" {'Tolerance':<{kw_width}}\t{o.tolerance}\n")
        else: # Write NONE if quality is None
            file.write(f" {'Quality':<{kw_width}}\tNONE\n")

        # Keep remaining options if they were parsed (less common)
        if hasattr(o, 'check_freq'): file.write(f" {'CheckFreq':<{kw_width}}\t{o.check_freq}\n")
        if hasattr(o, 'max_check'): file.write(f" {'MaxCheck':<{kw_width}}\t{o.max_check}\n")
        if hasattr(o, 'damp_limit'): file.write(f" {'DampLimit':<{kw_width}}\t{o.damp_limit}\n")
        # MAP option ignored

    def _write_coordinates(self, file):
        nodes_with_coords = sorted([
            (n.id, n.x_coord, n.y_coord) for n in self.network.get_all_nodes().values()
            if n.x_coord is not None and n.y_coord is not None
        ])
        if not nodes_with_coords: return
        self._write_section_header(file, "COORDINATES")
        file.write(f";{'Node':<16}\t{'X-Coord':<16}\t{'Y-Coord':<16}\n")
        file.write(";" + "-"*15 + "\t" + "-"*15 + "\t" + "-"*15 + "\n")

        for node_id, x, y in nodes_with_coords:
             line = (f" {self._format_field(node_id, 'id', is_text=True)}"
                     f"\t{self._format_field(x, 'coord', 2)}"
                     f"\t{self._format_field(y, 'coord', 2)}")
             file.write(f"{line}\n")


    def _write_vertices(self, file):
        links_with_vertices = sorted([
            (link.id, link.vertices) for link in self.network.get_all_links().values() if link.vertices
        ])
        if not links_with_vertices: return
        self._write_section_header(file, "VERTICES")
        file.write(f";{'Link':<16}\t{'X-Coord':<16}\t{'Y-Coord':<16}\n")
        file.write(";" + "-"*15 + "\t" + "-"*15 + "\t" + "-"*15 + "\n")

        for link_id, vertices in links_with_vertices:
            link_id_f = self._format_field(link_id, 'id', is_text=True)
            for vertex in vertices:
                line = (f" {link_id_f}"
                        f"\t{self._format_field(vertex.x, 'coord', 2)}"
                        f"\t{self._format_field(vertex.y, 'coord', 2)}")
                file.write(f"{line}\n")


    def _write_labels(self, file):
        if not self.network.labels: return
        self._write_section_header(file, "LABELS")
        file.write(f";{'X-Coord':<16}\t{'Y-Coord':<16}\t{'Label Text (quoted)'}\t{'Anchor Node (Optional)'}\n")
        file.write(";" + "-"*15 + "\t" + "-"*15 + "\t" + "-"*20 + "\t" + "-"*15 + "\n")


        # Sort labels? Maybe by coordinates?
        for label in self.network.labels:
             # Ensure text is quoted
             quoted_text = f'"{label.text}"'

             line = (f" {self._format_field(label.x, 'coord', 2)}"
                     f"\t{self._format_field(label.y, 'coord', 2)}"
                     f"\t{quoted_text:<22}") # Give quoted text some space

             if label.anchor_node:
                 line += f"\t{self._format_field(label.anchor_node, 'node', is_text=True)}"
             # No else needed, omit if None

             file.write(f"{line}\n")


    def _write_backdrop(self, file):
        b = self.network.backdrop
        has_backdrop = (b.dimensions is not None or b.units is not None or
                        b.file is not None or b.offset is not None)
        if not has_backdrop: return
        self._write_section_header(file, "BACKDROP")
        kw_width = 12

        if b.dimensions: file.write(f" {'DIMENSIONS':<{kw_width}}\t{b.dimensions[0]} {b.dimensions[1]} {b.dimensions[2]} {b.dimensions[3]}\n")
        if b.units: file.write(f" {'UNITS':<{kw_width}}\t{b.units}\n")
        if b.file: file.write(f" {'FILE':<{kw_width}}\t{b.file}\n")
        if b.offset: file.write(f" {'OFFSET':<{kw_width}}\t{b.offset[0]} {b.offset[1]}\n")


    