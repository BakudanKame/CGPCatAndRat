var Vec2D = (function(){
  var create = function(x, y){
    var obj = Object.create(def);
    obj.setXY(x, y);

    return obj;
  };


  var def ={
    _x: 1,
    _y: 0,

    getX: function()
    {
      return this._x;
    },

    setX: function(value)
    {
      this._x = value;
    },

    getY: function()
    {
      return this._y;
    },

    setY: function(value)
    {
      this._y = value;
    },

    setXY: function(x, y)
    {
      this._x = x;
      this._y = y;
    },

    getLength: function()
    {
      return Math.sqrt(this._x * this._x + this._y * this._y);
    },

    setLength: function(length)
    {
      var angle = this.getAngle();
      this._x = Math.cos(angle) * length;
      this._y = Math.sin(angle) * length;
    },

    getAngle: function()
    {
      return Math.atan2(this._y, this._x);
    },

    setAngle: function(angle)
    {
      var length = this.getLength();
      this._x = Math.cos(angle) * length;
      this._y = Math.sin(angle) * length;
    },

    add: function(vector)
    {
      this._x += vector.getX();
      this._y += vector.getY();
    },

    sub: function(vector)
    {
      this._x -= vector.getX();
      this._y -= vector.getY();
    },

    mul: function(value)
    {
      this._x *= value;
      this._y *= value;
    },

    div: function(value)
    {
      this._x /= value;
      this._y /= value;
    }
  };

  return {create:create};
}());


function catStrat4(cx, cy, rx, ry, Lx, Ly, ratThrustX, ratThrustY, catMaxThrust, losAngOld,  losLenOld, init4){

      var angle = 0;
      var nsep = 0;
      const N = 1
      var losAngleOld;
      var losAngleNew;
      var losLengthOld;
      var losLengthNew;
      var ratThrust = Vec2D.create(0, 0);
      ratThrust.setXY(ratThrustX, ratThrustY);
      const direction = Math.PI * 0.5

      var x = cx-rx;
      var y = cy-ry;
      x = (x > Lx/2) ? (x-Lx) : ((x<-Lx/2) ? (x+Lx) : x);
      y = (y>Ly/2) ? (y-Ly) : ((y<-Ly/2) ? (y+Ly) : y);
      nsep = (Math.pow(x,2)+Math.pow(y,2))/Lx/Ly;
      angle = Math.atan2(y,x);

      if (init4 == 1) {
        losAngleOld = angle
        losAngleNew = losAngleOld;
        losLengthOld = nsep
        losLengthNew = losLengthOld;
      }else{
        losAngleOld = losAngOld;
        losAngleNew = angle
        losLengthOld = losLenOld
        losLengthNew = nsep
      }

      var lineOfSight_rate = losAngleNew - losAngleOld;
      var closingVelocity =  losLengthOld - losLengthNew;



      var n_T = ratThrust.getLength() * Math.cos(losAngleNew + (0.5 * Math.PI) - ratThrust.getAngle());

      var lateralAccelerationP1 = lineOfSight_rate * N * closingVelocity
      var lateralAccelerationP2 = n_T * (0.5 * N)
      var lateralAcceleration = Vec2D.create(0, 0);
      lateralAcceleration.setLength(lateralAccelerationP1 + lateralAccelerationP2);
      if (ratThrust.getAngle() > losAngleNew) {
        lateralAcceleration.setAngle(losAngleNew + direction);
      }else {
        lateralAcceleration.setAngle(losAngleNew - direction);
      }
      var los_thrust = Vec2D.create(0, 0);
      los_thrust.setLength(Math.sqrt((Math.pow(800, 2)) - (Math.pow(lateralAcceleration.getLength(), 2))));
      los_thrust.setAngle(losAngleNew + Math.PI);
      lateralAcceleration.add(los_thrust);
      var thrustArray = [lateralAcceleration.getX(), lateralAcceleration.getY(), angle, nsep];
      return thrustArray;
};
