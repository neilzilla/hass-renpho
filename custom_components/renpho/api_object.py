from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel

class DeviceBind(BaseModel):
    id: int
    mac: str
    scale_name: str
    demo: str
    hw_ble_version: int
    device_type: int
    hw_software_version: int
    created_at: str
    uuid: str
    b_user_id: int
    internal_model: str
    wifi_name: str
    product_category: int

class UserResponse(BaseModel):
    status_code: str
    status_message: str
    terminal_user_session_key: str
    device_binds_ary: List[DeviceBind]
    new_bodyage_logic_flag: int
    cooling_period_flag: int
    id: int
    email: str
    account_name: str
    gender: int
    height: float
    height_unit: int
    waistline: int
    hip: int
    person_type: int
    category_type: int
    weight_unit: int
    current_goal_weight: float
    weight_goal_unit: int
    weight_goal: float
    locale: str
    birthday: str
    weight_goal_date: str
    avatar_url: str
    weight: float
    facebook_account: str
    twitter_account: str
    line_account: str
    sport_goal: int
    sleep_goal: int
    bodyfat_goal: float
    initial_weight: float
    initial_bodyfat: float
    area_code: str
    method: int
    user_code: str
    agree_flag: int
    reach_goal_weight_flag: int
    reach_goal_bodyfat_flag: int
    set_goal_at: int
    sell_flag: int
    allow_notification_flag: int
    phone: str
    region_code: str
    dump_flag: int
    weighing_mode: int
    password_present_flag: int
    stature: float
    custom: str
    index_extension: int
    person_body_shape: int
    person_goal: int
    accuracy_flag: int

class MeasurementDetail(BaseModel):
    id: int
    b_user_id: int
    time_stamp: int
    created_at: str
    created_stamp: int
    scale_type: int
    scale_name: str
    mac: str
    gender: int
    height: int
    height_unit: int
    birthday: str
    category_type: int
    person_type: int
    weight: float
    bodyfat: Optional[float] = None
    water: Optional[float] = None
    bmr: Optional[int] = None
    weight_unit: int
    bodyage: Optional[int] = None
    muscle: Optional[float] = None
    bone: Optional[float] = None
    subfat: Optional[float] = None
    visfat: Optional[int] = None
    bmi: float
    sinew: Optional[float] = None
    protein: Optional[float] = None
    body_shape: int
    fat_free_weight: Optional[float] = None
    resistance: Optional[int] = None
    sec_resistance: Optional[int] = None
    internal_model: str
    actual_resistance: Optional[int] = None
    actual_sec_resistance: Optional[int] = None
    heart_rate: Optional[int] = None
    cardiac_index: Optional[int] = None
    method: int
    sport_flag: int
    left_weight: Optional[float] = None
    waistline: Optional[float] = None
    hip: Optional[float] = None
    local_created_at: str
    time_zone: Optional[str] = None
    right_weight: Optional[float] = None
    accuracy_flag: int
    bodyfat_left_arm: Optional[float] = None
    bodyfat_left_leg: Optional[float] = None
    bodyfat_right_leg: Optional[float] = None
    bodyfat_right_arm: Optional[float] = None
    bodyfat_trunk: Optional[float] = None
    sinew_left_arm: Optional[float] = None
    sinew_left_leg: Optional[float] = None
    sinew_right_arm: Optional[float] = None
    sinew_right_leg: Optional[float] = None
    sinew_trunk: Optional[float] = None
    resistance20_left_arm: Optional[int] = None
    resistance20_left_leg: Optional[int] = None
    resistance20_right_leg: Optional[int] = None
    resistance20_right_arm: Optional[int] = None
    resistance20_trunk: Optional[int] = None
    resistance100_left_arm: Optional[int] = None
    resistance100_left_leg: Optional[int] = None
    resistance100_right_arm: Optional[int] = None
    resistance100_right_leg: Optional[int] = None
    resistance100_trunk: Optional[int] = None
    remark: Optional[str] = None
    score: Optional[int] = None
    pregnant_flag: Optional[int] = None
    stature: Optional[int] = None
    category: Optional[int] = None
    sea_waist: Optional[float] = None
    sea_hip: Optional[float] = None
    sea_whr_value: Optional[float] = None
    sea_chest: Optional[float] = None
    sea_abdomen: Optional[float] = None
    sea_neck: Optional[float] = None
    sea_left_arm: Optional[float] = None
    sea_right_arm: Optional[float] = None
    sea_left_thigh: Optional[float] = None
    sea_right_thigh: Optional[float] = None
    origin_resistances: Optional[str] = None


class MeasurementResponse(BaseModel):
    status_code: str
    status_message: str
    last_at: int
    previous_flag: int
    previous_at: int
    measurements: List[MeasurementDetail]


class Users(BaseModel):
    scale_user_id: str
    user_id: str
    mac: str
    index: int
    key: int
    method: int

class GirthGoal(BaseModel):
    girth_goal_id: int
    user_id: int
    girth_type: str
    setup_goal_at: int
    goal_value: float
    goal_unit: int
    initial_value: float
    initial_unit: int
    finish_goal_at: int
    finish_value: float
    finish_unit: int

class GirthGoalsResponse(BaseModel):
    status_code: str
    status_message: str
    terminal_user_session_key: str
    girth_goals: List[GirthGoal]
    new_bodyage_logic_flag: int
    cooling_period_flag: int
    id: int
    email: str
    account_name: str
    gender: int
    height: float
    height_unit: int
    waistline: int
    hip: int
    person_type: int
    category_type: int
    weight_unit: int
    current_goal_weight: float
    weight_goal_unit: int
    weight_goal: float
    locale: str
    birthday: str
    weight_goal_date: str
    avatar_url: str
    weight: float
    facebook_account: str
    twitter_account: str
    line_account: str
    sport_goal: int
    sleep_goal: int
    bodyfat_goal: float
    initial_weight: float
    initial_bodyfat: float
    area_code: str
    method: int
    user_code: str
    agree_flag: int
    reach_goal_weight_flag: int
    reach_goal_bodyfat_flag: int
    set_goal_at: int
    sell_flag: int
    allow_notification_flag: int
    phone: str
    region_code: str
    dump_flag: int
    weighing_mode: int
    password_present_flag: int
    stature: float
    custom: str
    index_extension: int
    person_body_shape: int
    person_goal: int
    accuracy_flag: int

class Girth(BaseModel):
    girth_id: int
    user_id: int
    time_stamp: int
    time_zone: str
    mac: str
    internal_model: str
    scale_name: str
    neck_value: float
    neck_unit: int
    shoulder_value: float
    shoulder_unit: int
    arm_value: float
    arm_unit: int
    chest_value: float
    chest_unit: int
    waist_value: float
    waist_unit: int
    hip_value: float
    hip_unit: int
    thigh_value: float
    thigh_unit: int
    calf_value: float
    calf_unit: int
    left_arm_value: float
    left_arm_unit: int
    left_thigh_value: float
    left_thigh_unit: int
    left_calf_value: float
    left_calf_unit: int
    right_arm_value: float
    right_arm_unit: int
    right_thigh_value: float
    right_thigh_unit: int
    right_calf_value: float
    right_calf_unit: int
    whr_value: float
    abdomen_value: float
    abdomen_unit: int
    custom: str
    custom_value: float
    custom_unit: int
    updated_at: int
    custom1: str
    custom_value1: float
    custom_unit1: int
    custom2: str
    custom_value2: float
    custom_unit2: int
    custom3: str
    custom_value3: float
    custom_unit3: int
    custom4: str
    custom_value4: float
    custom_unit4: int
    custom5: str
    custom_value5: float
    custom_unit5: int

class GirthResponse(BaseModel):
    status_code: str
    status_message: str
    terminal_user_session_key: str
    girths: List[Girth]
    deleted_girth_ids: List[int]
    last_updated_at: int
