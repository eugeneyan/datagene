class AddGameToAxis < ActiveRecord::Migration
  def change
  	add_column :axes, :game_type, :integer
  end
end
