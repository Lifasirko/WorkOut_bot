from aiogram.utils.callback_data import CallbackData

# ______________________________________________ CallbackData загальна ______________________________________________ #

payment_callback = CallbackData("pay", "id")

get_description_callback = CallbackData("description", "id")

get_referral_link_callback = CallbackData("get_referral_link", "id")

# ________________________________________________ CallbackData опцій ________________________________________________ #

options_callback = CallbackData("options", "type")

additional_options_callback = CallbackData("additional_options", "type", "updating_user_id")

children_menu_callback = CallbackData("children_menu", "id")

get_parent_link_callback = CallbackData("get_parent_link", "id")

set_children_callback = CallbackData("set_children", "id")

choose_children_callback = CallbackData("choose_children", "child_id", "child_name")

set_children_workout_callback = CallbackData("set_children_workout", "child_id", "child_name")

get_children_statistics_callback = CallbackData("get_children_statistics_callback", "child_id")

get_children_finish_workout_callback = CallbackData("get_children_finish_workout_callback", "child_id")

# ______________________________________________ CallbackData тренувань ______________________________________________ #

# back_callback = CallbackData("back", "id")

# choose_workout_callback = CallbackData("choose_workout", "id")

choose_program_callback = CallbackData("choose_program", "id")

# workout_list_callback = CallbackData("workout_list", "workout_id")

# workout_callback = CallbackData("workout", "workout_id")

start_workout_callback = CallbackData("start_workout", "program_id", "workout_id", "ex_number")

continue_workout_callback = CallbackData("continue", "workout_id", "exercise_id", "set_number")

finish_workout_callback = CallbackData("finish_workout", "workout_id", "exercise_id", "set_number")

exercises_list_callback = CallbackData("exercises_list", "exercise_id")

# exercise_callback = CallbackData("exercise", "task_n")

start_exercise_callback = CallbackData("start_exercise", "exercise_id")

# done_exercise_callback = CallbackData("done_exercise", "exercise_id")

# next_exercises_callback = CallbackData("next_exercise", "exercise_id")

pause_callback = CallbackData("pause", "workout_id", "exercise_id", "ex_number", "set_number")

pause_between_sets_callback = CallbackData("pause_between_sets", "workout_id", "exercise_id", "ex_number", "set_number",
                                           "from_call")

# _____________________________________________ CallbackData нагадувань _____________________________________________ #

plan_next_workout_callback = CallbackData("plan_workout", "user_id", "workout_id")

workout_schedule_callback = CallbackData("workout_schedule", "updating_user_id")

# plan_morning_workout_callback = CallbackData("plan_workout", "user_id", "workout_id")


# _____________________________________________ CallbackData інфо юзерів _____________________________________________ #

change_user_data_callback = CallbackData("change_user_data_callback", "updating_user_id")

change_user_name_callback = CallbackData("change_user_name_callback", "updating_user_id")

change_user_timezone_callback = CallbackData("change_user_timezone_callback", "updating_user_id")

change_user_birthday_callback = CallbackData("change_user_birthday_callback", "updating_user_id")

change_user_sex_male_fem_no_callback = CallbackData("change_user_sex_male_callback", "updating_user_id", "sex")

change_user_sex_callback = CallbackData("change_user_sex_callback", "updating_user_id")

change_user_level_callback = CallbackData("change_user_level_callback", "updating_user_id")

change_user_level_low_mid_high_callback = CallbackData("change_user_level_low_mid_high_callback", "level")

# __________________________________________ CallbackData для работы с меню __________________________________________ #


# Создаем CallbackData-объекты, которые будут нужны для работы с меню choose_program_menu.
menu_cd = CallbackData("show_menu", "level", "program_id", "workout_id", "exercise_id")
start_exercise = CallbackData("start", "exercise_id")

workout_menu_callback = CallbackData("start_exercise", "workout_id", "exercise_id", "ex_number", "set_number")
start_new_set_callback = CallbackData("start_new_set", "workout_id", "exercise_id", "set_number")

# ____________________________________ CallbackData для редактирования тренировок ____________________________________ #


workout_settings_callback = CallbackData("workout_settings_callback", "user_id")

program_settings_choose_set_callback = CallbackData("program_settings_choose_set_callback", "user_id")

workout_settings_choose_set_callback = CallbackData("workout_settings_choose_set_callback", "user_id")

exercise_settings_choose_set_callback = CallbackData("exercise_settings_choose_set_callback", "user_id")

add_new_program_callback = CallbackData("add_new_program_callback", "user_id")

change_program_callback = CallbackData("change_program_callback", "user_id")

change_program_workout_callback = CallbackData("change_program_workout_callback", "user_id")

set_program_name_callback = CallbackData("set_program_name_callback", "user_id", "program_id")

set_program_access_callback = CallbackData("set_program_access_callback", "user_id", "program_id", "access")

set_program_is_morning_callback = CallbackData("set_program_is_morning_callback", "user_id", "program_id", "morning")

set_program_level_callback = CallbackData("set_program_level_callback", "user_id", "program_id", "level")

set_program_sex_callback = CallbackData("set_program_sex_callback", "user_id", "program_id", "sex")

set_program_age_callback = CallbackData("set_program_age_callback", "user_id", "program_id", "age")

set_program_is_random_callback = CallbackData("set_program_is_random_callback", "user_id", "program_id")

set_program_back_callback = CallbackData("set_program_back_callback", "user_id", "program_id")

add_new_workout_callback = CallbackData("add_new_workout_callback", "user_id")

change_workout_callback = CallbackData("change_workout_callback", "user_id")

change_workout_exercise_callback = CallbackData("change_workout_exercise_callback", "user_id")

set_workout_name_callback = CallbackData("set_workout_name", "user_id", "workout_id", "workout_name")

set_workout_frequency_callback = CallbackData("set_workout_frequency", "user_id", "workout_id", "workout_frequency")

add_new_exercise_callback = CallbackData("add_new_exercise_callback", "user_id")

change_exercise_callback = CallbackData("change_exercise_callback", "user_id")

set_exercise_name_callback = CallbackData("set_exercise_name_callback", "user_id", "exercise_id", "exercise_name")

set_exercise_duration_callback = CallbackData("set_exercise_duration_callback", "user_id", "exercise_id",
                                              "exercise_duration")

set_exercise_definition_callback = CallbackData("set_exercise_definition_callback", "user_id", "exercise_id",
                                                "exercise_definition")

set_exercise_file_callback = CallbackData("set_exercise_file_callback", "user_id", "exercise_id",
                                          "exercise_file")

choose_exercise_to_change_callback = CallbackData("choose_exercise_to_change", "user_id", "exercise_id")

