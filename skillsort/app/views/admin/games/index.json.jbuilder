json.array!(@games) do |game|
  json.extract! game, :id, :user_id, :version, :game_type, :result
  json.url game_url(game, format: :json)
end
