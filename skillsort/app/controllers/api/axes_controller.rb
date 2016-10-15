module Api
  class AxesController < ApplicationController


    def index
      @axes = if game_type = params[:game_type]
                Axis.active.where( game_type: game_type ).select( 'id, name, description' )
              else
                Axis.active.select( 'id, name, description' )
              end

      render json: @axes, status: 200
    end
  end
end