from .sql_memory import build_memory


memory_map = {
  "sql_buffer_memory": build_memory,
}

memory = memory_map["sql_buffer_memory"]
memory(chat_args)