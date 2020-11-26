__all__ = ['proNav']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['Vec2D', 'catStrat4'])
@Js
def PyJsHoisted_catStrat4_(cx, cy, rx, ry, Lx, Ly, ratThrustX, ratThrustY, catMaxThrust, losAngOld, losLenOld, init4, this, arguments, var=var):
    var = Scope({'cx':cx, 'cy':cy, 'rx':rx, 'ry':ry, 'Lx':Lx, 'Ly':Ly, 'ratThrustX':ratThrustX, 'ratThrustY':ratThrustY, 'catMaxThrust':catMaxThrust, 'losAngOld':losAngOld, 'losLenOld':losLenOld, 'init4':init4, 'this':this, 'arguments':arguments}, var)
    var.registers(['losLengthOld', 'lateralAccelerationP1', 'losAngOld', 'catMaxThrust', 'ratThrust', 'N', 'init4', 'closingVelocity', 'thrustArray', 'ratThrustX', 'rx', 'lateralAcceleration', 'y', 'angle', 'ratThrustY', 'n_T', 'direction', 'lineOfSight_rate', 'x', 'los_thrust', 'Lx', 'nsep', 'lateralAccelerationP2', 'cy', 'losAngleNew', 'losAngleOld', 'ry', 'cx', 'losLenOld', 'losLengthNew', 'Ly'])
    var.put('angle', Js(0.0))
    var.put('nsep', Js(0.0))
    var.put('N', Js(1.0))
    pass
    pass
    pass
    pass
    var.put('ratThrust', var.get('Vec2D').callprop('create', Js(0.0), Js(0.0)))
    var.get('ratThrust').callprop('setXY', var.get('ratThrustX'), var.get('ratThrustY'))
    var.put('direction', (var.get('Math').get('PI')*Js(0.5)))
    var.put('x', (var.get('cx')-var.get('rx')))
    var.put('y', (var.get('cy')-var.get('ry')))
    var.put('x', ((var.get('x')-var.get('Lx')) if (var.get('x')>(var.get('Lx')/Js(2.0))) else ((var.get('x')+var.get('Lx')) if (var.get('x')<((-var.get('Lx'))/Js(2.0))) else var.get('x'))))
    var.put('y', ((var.get('y')-var.get('Ly')) if (var.get('y')>(var.get('Ly')/Js(2.0))) else ((var.get('y')+var.get('Ly')) if (var.get('y')<((-var.get('Ly'))/Js(2.0))) else var.get('y'))))
    var.put('nsep', (((var.get('Math').callprop('pow', var.get('x'), Js(2.0))+var.get('Math').callprop('pow', var.get('y'), Js(2.0)))/var.get('Lx'))/var.get('Ly')))
    var.put('angle', var.get('Math').callprop('atan2', var.get('y'), var.get('x')))
    if (var.get('init4')==Js(1.0)):
        var.put('losAngleOld', var.get('angle'))
        var.put('losAngleNew', var.get('losAngleOld'))
        var.put('losLengthOld', var.get('nsep'))
        var.put('losLengthNew', var.get('losLengthOld'))
    else:
        var.put('losAngleOld', var.get('losAngOld'))
        var.put('losAngleNew', var.get('angle'))
        var.put('losLengthOld', var.get('losLenOld'))
        var.put('losLengthNew', var.get('nsep'))
    var.put('lineOfSight_rate', (var.get('losAngleNew')-var.get('losAngleOld')))
    var.put('closingVelocity', (var.get('losLengthOld')-var.get('losLengthNew')))
    var.put('n_T', (var.get('ratThrust').callprop('getLength')*var.get('Math').callprop('cos', ((var.get('losAngleNew')+(Js(0.5)*var.get('Math').get('PI')))-var.get('ratThrust').callprop('getAngle')))))
    var.put('lateralAccelerationP1', ((var.get('lineOfSight_rate')*var.get('N'))*var.get('closingVelocity')))
    var.put('lateralAccelerationP2', (var.get('n_T')*(Js(0.5)*var.get('N'))))
    var.put('lateralAcceleration', var.get('Vec2D').callprop('create', Js(0.0), Js(0.0)))
    var.get('lateralAcceleration').callprop('setLength', (var.get('lateralAccelerationP1')+var.get('lateralAccelerationP2')))
    if (var.get('ratThrust').callprop('getAngle')>var.get('losAngleNew')):
        var.get('lateralAcceleration').callprop('setAngle', (var.get('losAngleNew')+var.get('direction')))
    else:
        var.get('lateralAcceleration').callprop('setAngle', (var.get('losAngleNew')-var.get('direction')))
    var.put('los_thrust', var.get('Vec2D').callprop('create', Js(0.0), Js(0.0)))
    var.get('los_thrust').callprop('setLength', var.get('Math').callprop('sqrt', (var.get('Math').callprop('pow', Js(800.0), Js(2.0))-var.get('Math').callprop('pow', var.get('lateralAcceleration').callprop('getLength'), Js(2.0)))))
    var.get('los_thrust').callprop('setAngle', (var.get('losAngleNew')+var.get('Math').get('PI')))
    var.get('lateralAcceleration').callprop('add', var.get('los_thrust'))
    var.put('thrustArray', Js([var.get('lateralAcceleration').callprop('getX'), var.get('lateralAcceleration').callprop('getY'), var.get('angle'), var.get('nsep')]))
    return var.get('thrustArray')
PyJsHoisted_catStrat4_.func_name = 'catStrat4'
var.put('catStrat4', PyJsHoisted_catStrat4_)
@Js
def PyJs_anonymous_0_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['def', 'create'])
    @Js
    def PyJs_anonymous_1_(x, y, this, arguments, var=var):
        var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
        var.registers(['x', 'y', 'obj'])
        var.put('obj', var.get('Object').callprop('create', var.get('def')))
        var.get('obj').callprop('setXY', var.get('x'), var.get('y'))
        return var.get('obj')
    PyJs_anonymous_1_._set_name('anonymous')
    var.put('create', PyJs_anonymous_1_)
    @Js
    def PyJs_anonymous_2_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get('_x')
    PyJs_anonymous_2_._set_name('anonymous')
    @Js
    def PyJs_anonymous_3_(value, this, arguments, var=var):
        var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
        var.registers(['value'])
        var.get(u"this").put('_x', var.get('value'))
    PyJs_anonymous_3_._set_name('anonymous')
    @Js
    def PyJs_anonymous_4_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get('_y')
    PyJs_anonymous_4_._set_name('anonymous')
    @Js
    def PyJs_anonymous_5_(value, this, arguments, var=var):
        var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
        var.registers(['value'])
        var.get(u"this").put('_y', var.get('value'))
    PyJs_anonymous_5_._set_name('anonymous')
    @Js
    def PyJs_anonymous_6_(x, y, this, arguments, var=var):
        var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
        var.registers(['x', 'y'])
        var.get(u"this").put('_x', var.get('x'))
        var.get(u"this").put('_y', var.get('y'))
    PyJs_anonymous_6_._set_name('anonymous')
    @Js
    def PyJs_anonymous_7_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        return var.get('Math').callprop('sqrt', ((var.get(u"this").get('_x')*var.get(u"this").get('_x'))+(var.get(u"this").get('_y')*var.get(u"this").get('_y'))))
    PyJs_anonymous_7_._set_name('anonymous')
    @Js
    def PyJs_anonymous_8_(length, this, arguments, var=var):
        var = Scope({'length':length, 'this':this, 'arguments':arguments}, var)
        var.registers(['length', 'angle'])
        var.put('angle', var.get(u"this").callprop('getAngle'))
        var.get(u"this").put('_x', (var.get('Math').callprop('cos', var.get('angle'))*var.get('length')))
        var.get(u"this").put('_y', (var.get('Math').callprop('sin', var.get('angle'))*var.get('length')))
    PyJs_anonymous_8_._set_name('anonymous')
    @Js
    def PyJs_anonymous_9_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        return var.get('Math').callprop('atan2', var.get(u"this").get('_y'), var.get(u"this").get('_x'))
    PyJs_anonymous_9_._set_name('anonymous')
    @Js
    def PyJs_anonymous_10_(angle, this, arguments, var=var):
        var = Scope({'angle':angle, 'this':this, 'arguments':arguments}, var)
        var.registers(['length', 'angle'])
        var.put('length', var.get(u"this").callprop('getLength'))
        var.get(u"this").put('_x', (var.get('Math').callprop('cos', var.get('angle'))*var.get('length')))
        var.get(u"this").put('_y', (var.get('Math').callprop('sin', var.get('angle'))*var.get('length')))
    PyJs_anonymous_10_._set_name('anonymous')
    @Js
    def PyJs_anonymous_11_(vector, this, arguments, var=var):
        var = Scope({'vector':vector, 'this':this, 'arguments':arguments}, var)
        var.registers(['vector'])
        var.get(u"this").put('_x', var.get('vector').callprop('getX'), '+')
        var.get(u"this").put('_y', var.get('vector').callprop('getY'), '+')
    PyJs_anonymous_11_._set_name('anonymous')
    @Js
    def PyJs_anonymous_12_(vector, this, arguments, var=var):
        var = Scope({'vector':vector, 'this':this, 'arguments':arguments}, var)
        var.registers(['vector'])
        var.get(u"this").put('_x', var.get('vector').callprop('getX'), '-')
        var.get(u"this").put('_y', var.get('vector').callprop('getY'), '-')
    PyJs_anonymous_12_._set_name('anonymous')
    @Js
    def PyJs_anonymous_13_(value, this, arguments, var=var):
        var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
        var.registers(['value'])
        var.get(u"this").put('_x', var.get('value'), '*')
        var.get(u"this").put('_y', var.get('value'), '*')
    PyJs_anonymous_13_._set_name('anonymous')
    @Js
    def PyJs_anonymous_14_(value, this, arguments, var=var):
        var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
        var.registers(['value'])
        var.get(u"this").put('_x', var.get('value'), '/')
        var.get(u"this").put('_y', var.get('value'), '/')
    PyJs_anonymous_14_._set_name('anonymous')
    var.put('def', Js({'_x':Js(1.0),'_y':Js(0.0),'getX':PyJs_anonymous_2_,'setX':PyJs_anonymous_3_,'getY':PyJs_anonymous_4_,'setY':PyJs_anonymous_5_,'setXY':PyJs_anonymous_6_,'getLength':PyJs_anonymous_7_,'setLength':PyJs_anonymous_8_,'getAngle':PyJs_anonymous_9_,'setAngle':PyJs_anonymous_10_,'add':PyJs_anonymous_11_,'sub':PyJs_anonymous_12_,'mul':PyJs_anonymous_13_,'div':PyJs_anonymous_14_}))
    return Js({'create':var.get('create')})
PyJs_anonymous_0_._set_name('anonymous')
var.put('Vec2D', PyJs_anonymous_0_())
pass
pass
pass


# Add lib to the module scope
proNav = var.to_python()